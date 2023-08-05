import sys
import sys
import os.path
import numpy as np
import pandas
import typing
import itertools
from statsmodels.tsa.api import VAR as vector_ar
import statsmodels.api as sm
from Sloth.predict import Arima
from sklearn.preprocessing import OneHotEncoder
from datetime import timedelta

from d3m.primitive_interfaces.base import PrimitiveBase, CallResult

from d3m import container, utils
from d3m.container import DataFrame as d3m_DataFrame, List
from d3m.metadata import hyperparams, base as metadata_base, params
from common_primitives import utils as utils_cp, dataset_to_dataframe as DatasetToDataFrame
from sri.common import config

import logging

__author__ = 'Distil'
__version__ = '1.0.1'
__contact__ = 'mailto:nklabs@newknowledge.com'

Inputs = container.pandas.DataFrame
Outputs = container.pandas.DataFrame


class Params(params.Params):
    pass


class Hyperparams(hyperparams.Hyperparams):
    datetime_index = hyperparams.Set(
        elements=hyperparams.Hyperparameter[int](-1),
        default=(),
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description='if multiple datetime indices exist, this HP specifies which to apply to training data. If \
            None, the primitive assumes there is only one datetime index. This HP can also specify multiple indices \
            which should be concatenated to form datetime_index')
    max_lags = hyperparams.UniformInt(
        lower=1,
        upper=sys.maxsize,
        default=10,
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description='maximum lag order to evluate to find model - eval criterion = AIC')
    seasonal = hyperparams.UniformBool(default=True, semantic_types=[
        'https://metadata.datadrivendiscovery.org/types/ControlParameter'],
                                       description="whether to perform ARIMA prediction with seasonal component")
    seasonal_differencing = hyperparams.UniformInt(lower=1, upper=365, default=1,
                                                   semantic_types=[
                                                       'https://metadata.datadrivendiscovery.org/types/ControlParameter'],
                                                   description='period of seasonal differencing to use in ARIMA perdiction')
    # weights_filter_value = hyperparams.Hyperparameter[typing.Union[str, None]](
    #     default = None,
    #     semantic_types = ['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
    #     description='value to select a filter from column filter index for which to return correlation  \
    #         coefficient matrix.')
    pass


class VARfix(PrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    """
        Primitive that applies a VAR multivariate forecasting model to time series data. The VAR
        implementation comes from the statsmodels library. The primitive is implemented with a number
        of hyperparameters to handle hierarchical indices and forecasting various timelines and
        intervals into the future.

        Training inputs: D3M dataset with multivariate time series (potentially structured according to
                                     hierarchical indices) and a time series index column.
        Outputs: D3M dataset with predicted observations for a length of 'n_periods' at a certain 'interval'
                 into the future
    """
    metadata = metadata_base.PrimitiveMetadata({
        # Simply an UUID generated once and fixed forever. Generated using "uuid.uuid4()".
        'id': "76b5a479-c209-4d94-92b5-7eba7a4d4499",
        'version': __version__,
        'name': "VARfix",
        # Keywords do not have a controlled vocabulary. Authors can put here whatever they find suitable.
        'keywords': ['Time Series'],
        'source': {
            'name': __author__,
            'contact': __contact__,
            'uris': [
                # Unstructured URIs.
                "https://github.com/NewKnowledge/TimeSeries-D3M-Wrappers",
            ],
        },
        # A list of dependencies in order. These can be Python packages, system packages, or Docker images.
        # Of course Python packages can also have their own dependencies, but sometimes it is necessary to
        # install a Python package first to be even able to run setup.py of another package. Or you have
        # a dependency which is not on PyPi.
        'installation': [
            config.INSTALLATION
        ],
        # The same path the primitive is registered with entry points in setup.py.
        'python_path': 'd3m.primitives.time_series_forecasting.vector_autoregression.VARfix',
        # Choose these from a controlled vocabulary in the schema. If anything is missing which would
        # best describe the primitive, make a merge request.
        'algorithm_types': [
            metadata_base.PrimitiveAlgorithmType.VECTOR_AUTOREGRESSION
        ],
        'primitive_family': metadata_base.PrimitiveFamily.TIME_SERIES_FORECASTING,
    })

    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self._params = {}

        # track metadata about times, targets, indices, grouping keys
        self.filter_idxs = None
        self._target_types = None
        self._targets = None
        self.times = None
        self.key = None
        self.integer_time = False
        self.target_indices = None

        # encodings of categorical variables
        self._cat_indices = []
        self._encoders = []
        self.categories = None

        # information about interpolation
        self.unique_indices = None
        self.interpolation_ranges = None

        # data needed to fit model and reconstruct predictions
        self._X_train = None
        self._mins = None
        self._lag_order = []
        self._values = None
        self._fits = []
        self._final_logs = None

    def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:
        '''
        fits VAR model. Evaluates different lag orders up to maxlags, eval criterion = AIC
        '''

        # log transformation for standardization, difference, drop NAs
        self._mins = [sequence.values.min() if sequence.values.min() < 0 else 0 for sequence in self._X_train]
        self._values = [sequence.apply(lambda x: x - min + 1) for sequence, min in zip(self._X_train, self._mins)]
        self._values = [np.log(sequence.values) for sequence in self._values]
        self._final_logs = [sequence[-1:, ] for sequence in self._values]
        self._values = [np.diff(sequence, axis=0) for sequence in self._values]

        models = [vector_ar(vals, dates=original.index) if vals.shape[1] > 1 \
                      else Arima(self.hyperparams['seasonal'], self.hyperparams['seasonal_differencing']) for
                  vals, original in zip(self._values, self._X_train)]
        for vals, model, original in zip(self._values, models, self._X_train):

            # iteratively try fewer lags if problems with matrix decomposition
            if vals.shape[1] > 1:
                lags = self.hyperparams['max_lags']
                while lags > 1:
                    try:
                        lags = model.select_order(maxlags=self.hyperparams['max_lags']).aic
                        logging.debug(
                            'Successfully performed model order selection. Optimal order = {} lags'.format(lags))
                        if lags == 0:
                            logging.debug('At least 1 coefficient is needed for prediction. Setting lag order to 1')
                            lags = 1
                            self._lag_order.append(lags)
                            self._fits.append(model.fit(lags))
                        else:
                            self._lag_order.append(lags)
                            self._fits.append(model.fit(lags))
                        break
                    except np.linalg.LinAlgError:
                        lags = lags // 2
                        logging.debug(
                            'Matrix decomposition error because max lag order is too high. Trying max lag order {}'.format(
                                lags))
                else:
                    lags = self.hyperparams['max_lags']
                    while lags > 1:
                        try:
                            self._fits.append(model.fit(lags))
                            self._lag_order.append(lags)
                            logging.debug('Successfully fit model with lag order {}'.format(lags))
                            break
                        except ValueError:
                            logging.debug(
                                'Value Error - lag order {} is too large for the model. Trying lag order {} instead'.format(
                                    lags, lags - 1))
                            lags -= 1
                    else:
                        self._fits.append(model.fit(lags))
                        self._lag_order.append(lags)
                        logging.debug('Successfully fit model with lag order {}'.format(lags))
            else:
                X_train = pandas.Series(data=vals.reshape((-1,)), index=original.index[:vals.shape[0]])
                model.fit(X_train)
                self._fits.append(model)
                self._lag_order.append(None)
        return CallResult(None)

    def get_params(self) -> Params:
        return self._params

    def set_params(self, *, params: Params) -> None:
        self.params = params

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        '''
        Sets primitive's training data

        Parameters
        ----------
        inputs_copy: input d3m_dataframe containing n columns of features

        '''
        inputs_copy = inputs.copy()

        # set datetime index
        times = inputs_copy.metadata.get_columns_with_semantic_type('https://metadata.datadrivendiscovery.org/types/Time') + \
                inputs_copy.metadata.get_columns_with_semantic_type('http://schema.org/DateTime')
        times = list(set(times))
        if len(times) != 1:
            raise ValueError(f"There are {len(times)} indices marked as datetime values. You must specify one index to use using +\
                             'datetime_index' hyperparameter.")
        self.times = [list(inputs_copy)[t] for t in times]

        # if datetime columns are integers, parse as # of days
        if 'http://schema.org/Integer' in inputs_copy.metadata.query_column(times[0])['semantic_types']:
            self.integer_time = True
            inputs_copy[self.times[0]] = pandas.to_datetime(inputs_copy[self.times[0]] - 1, unit='D')
        else:
            inputs_copy[self.times[0]] = pandas.to_datetime(inputs_copy[self.times[0]], unit='s')

        # mark key and categorical variables
        self.key = inputs_copy.metadata.get_columns_with_semantic_type(
            'https://metadata.datadrivendiscovery.org/types/PrimaryKey')
        cat = inputs_copy.metadata.get_columns_with_semantic_type(
            'https://metadata.datadrivendiscovery.org/types/CategoricalData')
        self.categories = cat.copy()

        # mark target variables
        self._targets = inputs_copy.metadata.get_columns_with_semantic_type(
            'https://metadata.datadrivendiscovery.org/types/TrueTarget')
        if not len(self._targets):
            self._targets = inputs_copy.metadata.get_columns_with_semantic_type(
                'https://metadata.datadrivendiscovery.org/types/Target')
        if not len(self._targets):
            self._targets = inputs_copy.metadata.get_columns_with_semantic_type(
                'https://metadata.datadrivendiscovery.org/types/SuggestedTarget')
        self._target_types = ['i' if 'http://schema.org/Integer' in inputs_copy.metadata.query_column(t)['semantic_types'] \
                                  else 'c' if 'https://metadata.datadrivendiscovery.org/types/CategoricalData' in \
                                              inputs_copy.metadata.query_column(t)['semantic_types'] else 'f' for t in
                              self._targets]
        self._targets = [list(inputs_copy)[t] for t in self._targets]

        # intelligently calculate grouping key order - by highest number of unique vals after grouping
        grouping_keys = inputs_copy.metadata.get_columns_with_semantic_type(
            'https://metadata.datadrivendiscovery.org/types/SuggestedGroupingKey')
        grouping_keys_counts = [inputs_copy.iloc[:, key_idx].nunique() for key_idx in grouping_keys]
        grouping_keys = [group_key for count, group_key in sorted(zip(grouping_keys_counts, grouping_keys))]
        grouping_keys.reverse()
        self.filter_idxs = [list(inputs_copy)[key] for key in grouping_keys]

        # convert categorical variables to 1-hot encoded
        [self.categories.remove(group_key) for group_key in grouping_keys]
        for c in self.categories:
            encoder = OneHotEncoder(handle_unknown='ignore')
            self._encoders.append(encoder)
            encoder.fit(inputs_copy.iloc[:, c].values.reshape(-1, 1))
            inputs_copy[list(inputs_copy)[c] + '_' + encoder.categories_[0]] = pandas.DataFrame(
                encoder.transform(inputs_copy.iloc[:, c].values.reshape(-1, 1)).toarray())
            self._cat_indices.append(np.arange(inputs_copy.shape[1] - len(encoder.categories_[0]), inputs_copy.shape[1]))

        # drop original categorical variables, index key
        drop_idx = self.categories + self.key
        inputs_copy.drop(columns=[list(inputs_copy)[idx] for idx in drop_idx], inplace=True)
        self._cat_indices = [arr - len(drop_idx) - 1 for arr in self._cat_indices]

        # check whether no grouping keys are labeled
        if len(grouping_keys) == 0:
            if sum(inputs_copy[self.times[0]].duplicated()) > 0:
                inputs_copy['temp_time_index_0'] = inputs_copy[self.times[0]]
                inputs_copy = inputs_copy.groupby(['temp_time_index_0']).agg('sum')
                self.unique_indices = [False]
            else:
                self.unique_indices = [True]
            inputs_copy = inputs_copy.set_index(self.times[0])
            inputs_copy = inputs_copy.interpolate(method='time', limit_direction='both')
            self._X_train = [inputs_copy]
            self.target_indices = [i for i, col_name in enumerate(list(inputs_copy)) if col_name in self._targets]

        else:
            # find interpolation range from outermost grouping key
            self.interpolation_ranges = inputs_copy.groupby(self.filter_idxs[0]).agg({self.times[0]: ['min', 'max']})

            # group by grouping keys -> group non-unique, re-index, interpolate
            self._X_train = [None for i in range(max(grouping_keys_counts))]
            self.unique_indices = [True for i in range(len(self._X_train))]
            for _, group in inputs_copy.groupby(self.filter_idxs):
                group_value = group[self.filter_idxs[0]].values[0]
                interpolation_range = self.interpolation_ranges.loc[group_value]
                training_idx = np.where(self.interpolation_ranges.index == group_value)[0][0]
                group = group.drop(columns=self.filter_idxs)

                # group non-unique time indices
                if sum(group[self.times[0]].duplicated()) > 0:
                    group['temp_time_index_0'] = group[self.times[0]]
                    group = group.groupby(['temp_time_index_0']).agg('sum')
                    self.unique_indices[training_idx] = False

                # re-index and interpolate
                group = group.set_index(self.times[0])
                min_date = self.interpolation_ranges.loc[group_value][self.times[0]]['min']
                max_date = self.interpolation_ranges.loc[group_value][self.times[0]]['max']
                group = group.reindex(pandas.date_range(min_date, max_date))
                group = group.interpolate(method='time', limit_direction='both')

                # add to training data under appropriate top-level grouping key
                self.target_indices = [i for i, col_name in enumerate(list(group)) if col_name in self._targets]
                if self._X_train[training_idx] is None:
                    self._X_train[training_idx] = group
                else:
                    self._X_train[training_idx] = pandas.concat([self._X_train[training_idx], group], axis=1)

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:

        """
        Produce primitive's prediction for future time series data

        Parameters
        ----------
        None

        Returns
        ----------
        Outputs
            The output is a data frame containing the d3m index and a forecast for each of the 'n_periods' future time periods,
            modified if desired by the 'interval' HP
            The default is a future forecast for each of the selected input variables. This can be modified to just one output
                variable with the associated HP
        """

        # parse datetime indices
        # if datetime columns are integers, parse as # of days
        if type(inputs[self.times[0]][0]) is not pandas._libs.tslibs.timestamps.Timestamp:
            if self.integer_time:
                inputs[self.times[0]] = pandas.to_datetime(inputs[self.times[0]] - 1, unit='D')
            else:
                inputs[self.times[0]] = pandas.to_datetime(inputs[self.times[0]], unit='s')

        # intelligently calculate grouping key order - by highest number of unique vals after grouping
        grouping_keys = inputs.metadata.get_columns_with_semantic_type(
            'https://metadata.datadrivendiscovery.org/types/SuggestedGroupingKey')

        # groupby learned filter_idxs and extract n_periods, interval and d3mIndex information
        n_periods, intervals, d3m_indices = self._calculate_prediction_intervals(inputs, grouping_keys)

        # produce future foecast using VAR / ARMA
        future_forecasts = [fit.forecast(vals[-fit.k_ar:], n) if vals.shape[1] > 1 \
                                else fit.predict(int(n)) for fit, vals, n in zip(self._fits, self._values, n_periods)]

        # undo differencing transformations
        future_forecasts = [np.exp(future_forecast.cumsum(axis=0) + final_logs).T if len(future_forecast.shape) is 1 \
                                else np.exp(future_forecast.cumsum(axis=0) + final_logs) for future_forecast, final_logs
                            in zip(future_forecasts, self._final_logs)]
        future_forecasts = [pandas.DataFrame(future_forecast) for future_forecast in future_forecasts]
        future_forecasts = [future_forecast.apply(lambda x: x + minimum - 1) if lag == 1 else future_forecast for
                            future_forecast, minimum, lag \
                            in zip(future_forecasts, self._mins, self._lag_order)]

        # convert categorical columns back to categorical labels
        for forecast in future_forecasts:
            for one_hot_cat, original_cat, enc, unique in zip(self._cat_indices, self.categories, self._encoders,
                                                              self.unique_indices):
                if unique:
                    # round categoricals
                    forecast[one_hot_cat] = forecast[one_hot_cat].apply(lambda x: x >= 1.5).astype(int)
                    # convert to categorical labels
                    forecast[list(inputs)[original_cat]] = enc.inverse_transform(forecast[one_hot_cat].values)
                    # remove one-hot encoded columns
                    forecast.drop(columns=one_hot_cat, inplace=True)
                else:
                    # round categoricals to whole numbers
                    forecast[one_hot_cat] = forecast[one_hot_cat].astype(int)

        # select predictions to return based on intervals
        key_names = [list(inputs)[k] for k in self.key]
        var_df = pandas.DataFrame([], columns=key_names + self._targets)
        for forecast, interval, idxs in zip(future_forecasts, intervals, d3m_indices):
            for row, col, d3m_idx in zip(interval, range(len(interval)), idxs):
                for r, i in zip(row, d3m_idx):
                    cols = [col + t for t in self.target_indices]
                    var_df.loc[var_df.shape[0]] = [i, *forecast.iloc[r][cols].values]
        var_df = d3m_DataFrame(var_df)
        var_df.iloc[:, 0] = var_df.iloc[:, 0].astype(int)

        # first column ('d3mIndex')
        col_dict = dict(var_df.metadata.query((metadata_base.ALL_ELEMENTS, 0)))
        col_dict['structural_type'] = type("1")
        col_dict['name'] = key_names[0]
        col_dict['semantic_types'] = (
        'http://schema.org/Integer', 'https://metadata.datadrivendiscovery.org/types/PrimaryKey',)
        var_df.metadata = var_df.metadata.update((metadata_base.ALL_ELEMENTS, 0), col_dict)

        # assign target metadata and round appropriately
        for (index, name), target_type in zip(enumerate(self._targets), self._target_types):
            col_dict = dict(var_df.metadata.query((metadata_base.ALL_ELEMENTS, index + 1)))
            col_dict['structural_type'] = type("1")
            col_dict['name'] = name
            col_dict['semantic_types'] = ('https://metadata.datadrivendiscovery.org/types/SuggestedTarget', \
                                          'https://metadata.datadrivendiscovery.org/types/TrueTarget',
                                          'https://metadata.datadrivendiscovery.org/types/Target')
            if target_type == 'i':
                var_df[name] = var_df[name].astype(int)
                col_dict['semantic_types'] += ('http://schema.org/Integer',)
            elif target_type == 'c':
                col_dict['semantic_types'] += ('https://metadata.datadrivendiscovery.org/types/CategoricalData',)
            else:
                col_dict['semantic_types'] += ('http://schema.org/Float',)
            var_df.metadata = var_df.metadata.update((metadata_base.ALL_ELEMENTS, index + 1), col_dict)
        return CallResult(var_df)

    def produce_weights(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:
        """
        Produce correlation coefficients (weights) for each of the terms used in the regression model

        Parameters
        ----------
        filter_value:   value to select a filter from column filter index for which to return correlation coefficient matrix. If None,
                        method returns most recent filter

        Returns
        ----------
        Outputs
            The output is a data frame containing columns for each of the terms used in the regression model. Each row contains the
            correlation coefficients for each term in the regression model. If there are multiple unique timeseries indices in the
            dataset there can be multiple rows in this output dataset. Terms that aren't included in a specific timeseries index will
            have a value of NA in the associated matrix entry.
        """

        # get correlation coefficients
        coef = [fit.coefs if vals.shape[1] > 1 else np.array([1]) for fit, vals in zip(self._fits, self._values)]

        # create column labels
        if self.hyperparams['weights_filter_value'] is not None:
            idx = np.where(np.sort(inputs.iloc[:, self.hyperparams['filter_index_one']].unique()) == self.hyperparams[
                'weights_filter_value'])[0][0]
            inputs_filtered = inputs.loc[
                inputs[list(inputs)[self.hyperparams['filter_index_one']]] == self.hyperparams['weights_filter_value']]
            cols = inputs_filtered.iloc[:, self.hyperparams['filter_index_two']].unique()
        else:
            idx = 0
            cols = list(self._X_train[0])

        # reshape matrix if multiple lags
        if self._lag_order > 1:
            vals = coef[idx].reshape(-1, coef[idx].shape[2])
            idx = [c + '_lag_order_' + str(order) for order in np.arange(coef[idx].shape[0]) + 1 for c in cols]
        else:
            vals = coef[idx][0]
            idx = cols
        return CallResult(pandas.DataFrame(vals, columns=cols, index=idx))

    def _calculate_prediction_intervals(self,
                                        inputs: Inputs,
                                        grouping_keys: typing.Sequence[int]) -> typing.Tuple[typing.Sequence[int],
                                                                                             typing.Sequence[
                                                                                                 typing.Sequence[int]],
                                                                                             typing.Sequence[
                                                                                                 typing.Sequence[
                                                                                                     typing.Any]]]:

        # check whether no grouping keys are labeled
        if len(grouping_keys) == 0:
            group_tuple = ((None, inputs),)
        else:
            group_tuple = inputs.groupby(self.filter_idxs)

        # groupby learned filter_idxs and extract n_periods, interval and d3mIndex information
        n_periods = [1 for i in range(len(self._X_train))]
        intervals = [None for i in range(len(self._X_train))]
        d3m_indices = [None for i in range(len(self._X_train))]
        for _, group in group_tuple:
            if len(grouping_keys) > 0:
                group_value = group[self.filter_idxs[0]].values[0]
                testing_idx = np.where(self.interpolation_ranges.index == group_value)[0][0]
            else:
                testing_idx = 0
            max_train_idx = self._X_train[testing_idx].index.max()
            local_intervals = self._discretize_time_difference(group[self.times[0]] - max_train_idx)

            # test for empty series (train setting)
            if max(local_intervals) <= 0:
                local_intervals = [0]
                idxs = [0]
            else:
                # TODO: grab training values for series who have index before max)
                local_intervals = [l - 1 if l > 0 else 0 for l in local_intervals]
                idxs = group.iloc[:, self.key[0]].values

            # save n_periods prediction information
            if n_periods[testing_idx] < max(local_intervals) + 1:
                n_periods[testing_idx] = max(local_intervals) + 1

            # save interval prediction information
            if intervals[testing_idx] is None:
                intervals[testing_idx] = [local_intervals]
            else:
                intervals[testing_idx].append(local_intervals)

            # save d3m indices prediction information
            if d3m_indices[testing_idx] is None:
                d3m_indices[testing_idx] = [idxs]
            else:
                d3m_indices[testing_idx].append(idxs)

        return n_periods, intervals, d3m_indices

    @classmethod
    def _discretize_time_difference(cls, time_differences: typing.Sequence[timedelta]) -> typing.Sequence[int]:

        SECONDS_PER_MINUTE = 60
        MINUTES_PER_HOUR = 60
        HOURS_PER_DAY = 24
        DAYS_PER_WEEK = 7
        DAYS_PER_MONTH = [30, 31]
        DAYS_PER_YEAR = 365

        # special case if differences are negative (training set)
        if time_differences.iloc[0].total_seconds() < 0:
            return [0]

        # determine unit of differencing between first two items (could take mode over whole list?)
        diff = time_differences.iloc[1] - time_differences.iloc[0] if len(time_differences) > 1 else \
        time_differences.iloc[0]
        if diff.total_seconds() % (SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY * DAYS_PER_YEAR) == 0:
            return time_differences.apply(lambda x: int(x.days / DAYS_PER_YEAR)).values
        elif diff.total_seconds() % (SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY * DAYS_PER_MONTH[0]) == 0 or \
                diff.total_seconds() % (SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY * DAYS_PER_MONTH[1]) == 0:
            return time_differences.apply(lambda x: int(x.days / DAYS_PER_MONTH[0])).values
        elif diff.total_seconds() % (SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY) == 0:
            return time_differences.apply(lambda x: x.days).values
        elif diff.total_seconds() % (SECONDS_PER_MINUTE * MINUTES_PER_HOUR) == 0:
            return time_differences.apply(lambda x: x.hours).values
        elif diff.total_seconds() % (SECONDS_PER_MINUTE) == 0:
            return time_differences.apply(lambda x: x.seconds).values
