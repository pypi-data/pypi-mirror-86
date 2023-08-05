import os

from d3m.metadata import hyperparams as meta_hyperparams

from sri.common import constants

class PSLHyperparams(meta_hyperparams.Hyperparams):
    '''
    The base class for PSL Hyperparams.
    '''
    psl_options = meta_hyperparams.Hyperparameter(
            description = 'General options to be blindly passed to the PSL CLI.',
            default = '',
            semantic_types = ['https://metadata.datadrivendiscovery.org/types/ControlParameter'])

    postgres_db_name = meta_hyperparams.Hyperparameter(
            description = 'The name of the PostgreSQL databse to use. If empty, Postgres will not be used.',
            default = 'psl_d3m',
            semantic_types = ['https://metadata.datadrivendiscovery.org/types/ControlParameter'])

    admm_iterations = meta_hyperparams.Bounded(
            description = 'The maximum number of ADMM iterations to run. If 0, the PSL default will be used.',
            default = 1000,
            lower = 0,
            upper = None,
            semantic_types = ['https://metadata.datadrivendiscovery.org/types/ControlParameter'])

    max_threads = meta_hyperparams.Bounded(
            description = 'The maximum number of threads PSL will use. If 0, the PSL default will be used.',
            default = 0,
            lower = 0,
            upper = None,
            semantic_types = ['https://metadata.datadrivendiscovery.org/types/ControlParameter'])

    jvm_memory = meta_hyperparams.Bounded(
            description = 'The amount of memory (as a percent of the system total) to initially allocate the JVM (-Xms).',
            default = constants.DEFAULT_MEMORY_PERCENT,
            lower = 0.01,
            upper = 1.00,
            semantic_types = ['https://metadata.datadrivendiscovery.org/types/ControlParameter'])
