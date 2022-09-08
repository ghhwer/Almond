from .bases import Engine
from pyspark.sql import SparkSession
from ..context import AlmondContext

from functools import reduce

def append_if_not_none_add_if_none(d, key, value):
    if (d is None):
        d = {key:value}
    else:
        d[key] = value
    return d


class NativeSparkEngine(Engine):
    def __init__(self, app_name='spark_almond_app', options=None):
        self.options=options
        self.engine_name = 'native_spark'
        self.app_name = app_name

    def init_engine(self):
        # Get Spark options set by AlmondContext.
        options = AlmondContext().get_config('spark_configs')
        # Check if we should enable hive support.
        enable_hive_support = AlmondContext().get_config('enable_hive_support')

        # Get any driver and executor extra java options 
        spark_driver_extra_java_options = AlmondContext().get_config('spark_driver_extra_java_options')
        spark_executor_extra_java_options = AlmondContext().get_config('spark_executor_extra_java_options')
        
        # Set them accordingly by adding it to the options
        if(spark_driver_extra_java_options is not None):
            extraDriverJavaOptions = ';'.join(spark_driver_extra_java_options)
            options = append_if_not_none_add_if_none(options, 'spark.driver.extraJavaOptions', extraDriverJavaOptions)
        
        if(spark_executor_extra_java_options is not None):
            extraExecutorJavaOptions = ';'.join(spark_executor_extra_java_options)
            options = append_if_not_none_add_if_none(options, 'spark.executor.extraJavaOptions', extraExecutorJavaOptions)

        # If any options, add them to the SparkSession 
        if (options is not None):
            spark_conf = reduce(
                lambda x, y: x.config(y[0], y[1]),
                options.items(),
                SparkSession.builder.appName(self.app_name)
            )
        else:
            spark_conf = SparkSession.builder.appName(self.app_name)
        # Add hive support if asked to do so
        if((enable_hive_support is not None) and (enable_hive_support == True)):
            spark_conf = spark_conf.enableHiveSupport()
        # Set the spark session !
        self.spark_session = spark_conf.getOrCreate()

    def get_engine_context(self):
        return self.spark_session

    def get_object(self, database_name, table_name, predicate=None, options=None):
        metadata = AlmondContext().get_metadata()
        
        # Format options
        push_options = options
        if (predicate is not None):
            if(type(push_options) == dict):
                push_options['predicate'] = predicate 
            else:
                push_options = {'predicate': predicate}
        
        # Get data
        return metadata.get_dataframe(database_name, table_name, options=options)

    def save_object(self, df, database_name, table_name, partition_col=None, options=None):
        # Normalize options
        if(options is None):
            options = {}

        # Get sb and metadata from context...
        metadata = AlmondContext().get_metadata()

        # Prepare Options
        write_format = options.get('write_format', 'parquet')
        write_mode = options.get('write_mode', 'overwrite')

        # Check table type is supported
        metadata.check_table_accept(df, database_name, table_name, write_mode, partition_col, write_format)
        # If no errors, commit to metadata!
        metadata.commit_dataframe(df, database_name, table_name, partition_col, write_mode, write_format)

    def close_session(self):
        self.spark_session.stop()
        pass