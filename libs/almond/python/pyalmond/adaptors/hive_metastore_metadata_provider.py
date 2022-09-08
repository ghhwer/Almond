from .bases import MetadataProvider
from .local_storage_base import LocalStorageBase
from .spark_engine import NativeSparkEngine
from ..context import AlmondContext

from .utils.spark_utils import save_as_table_parquet_hive_metastore

import re
import json

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

class HiveMetadata(MetadataProvider):
    adaptor_compatibility_list = [LocalStorageBase, NativeSparkEngine]
    def __init__(self, options={}):
        self.options = options

    def init_metadata_provider(self):
        pass

    def get_database_info(self, database_name, options=None):
        return None

    def get_dataframe(self, database_name, table_name, options=None):
        spark = AlmondContext().get_engine().get_engine_context()
        if(options is not None):
            if(options.get('predicate', None) is not None):
                return spark.sql(f'select * from {database_name}.{table_name}').filter(options.get('predicate'))
        return spark.sql(f'select * from {database_name}.{table_name}')

    def database_exists(self, database_name, options=None):
        spark = AlmondContext().get_engine().get_engine_context()
        return spark.catalog.databaseExists(database_name)

    def add_or_update_database(self, database_name, description=False):
        spark = AlmondContext().get_engine().get_engine_context()
        spark.sql(F'CREATE DATABASE IF NOT EXISTS {database_name}')

    def delete_database(self, database_name, options=None):
        spark = AlmondContext().get_engine().get_engine_context()
        spark.sql(F'DROP DATABASE IF EXISTS {database_name}')

    def get_table_info(self, database_name, table_name, options=None):
        spark = AlmondContext().get_engine().get_engine_context()
        return spark.sql(F'SHOW CREATE TABLE {database_name}.{table_name}')

    def delete_table(self, database_name, table_name, options=None):
        spark = AlmondContext().get_engine().get_engine_context()
        return spark.sql(F'DROP TABLE {database_name}.{table_name}')

    def table_exists(self, database_name, table_name, options=None):
        spark = AlmondContext().get_engine().get_engine_context()
        return spark._jsparkSession.catalog().tableExists(database_name, table_name)

    def check_table_accept(self, df, database_name, table_name, partition_col, write_mode, write_format, options=None):
        # First we check if table exists
        if self.database_exists(database_name):
            if self.table_exists(database_name, table_name):
                spark = AlmondContext().get_engine().get_engine_context()
                df_sto = spark.sql(f'SELECT * FROM {database_name}.{table_name}') 
                # Stored info
                df_stored_schema = json.loads(df_sto.schema.json())
                df_saving_schema = json.loads(df.schema.json())
                schema_match = (ordered(df_saving_schema) == ordered(df_stored_schema))
                #parti_col_match = (ordered(partition_col) == ordered(df_stored_part_json))
                if( schema_match ):#and parti_col_match ):
                    return True
                else:
                    raise ValueError(f'Dataframe does not match stored info: schema_match={schema_match}')#parti_col_match={parti_col_match}')
            else:
                return True
        else:
            raise ValueError(f'Database {database_name} does not exist!')

    def commit_dataframe(self, df, database_name, table_name, partition_col, write_mode, write_format, options=None):
        spark = AlmondContext().get_engine().get_engine_context()
        storage_base = AlmondContext().get_storage_base()
        
        fs_path = storage_base.build_storage_string(database_name, table_name)

        if (write_format == 'parquet'):
            save_as_table_parquet_hive_metastore(
                spark, df, database_name, table_name, partition_col, self, write_mode
            )
            storage_base.commit(database_name, table_name)
        else:
            raise NotImplementedError(f'Cannot write {write_format}')
    
    def close_session(self):
        pass