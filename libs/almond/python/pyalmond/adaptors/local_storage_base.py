from .bases import StorageBase
from .spark_engine import NativeSparkEngine
from ..context import AlmondContext
import os

import re
import shutil

class LocalStorageBase(StorageBase):
    def __init__(self, options={}):
        self.options = options
        self.storage_base = 'local'
        self.local_database_dir = self.options.get('local_database_dir', f'{os.getcwd()}/almond_local_data')
        self.should_set_derby_dir = self.options.get('should_set_derby_dir', True)

    def __local_storage_cleanup(self):
        if (self.options.get('is_ephemeral', False)):
            try:
                shutil.rmtree(self.local_database_dir)
            except:
                pass

    def init_storage_base(self):
        if (self.local_database_dir is not None):
            AlmondContext().set_config('spark_configs', {'spark.sql.warehouse.dir':f'{self.local_database_dir}/spark-warehouse'})
        if (self.options.get('enable_hive_support', False)):
            AlmondContext().set_config('enable_hive_support', True)
            if(self.should_set_derby_dir):
                AlmondContext().set_config('spark_driver_extra_java_options', [f'-Dderby.system.home={self.local_database_dir}/derby-system-home'])
        self.__local_storage_cleanup()

    def build_storage_string(self, database, table, options=None):
        return None
    def commit(self, database, table, options=None):
        pass
    def close_session(self):
        self.__local_storage_cleanup()