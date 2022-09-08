from abc import ABC, abstractmethod

def check_compatibility(clist, adaptor, me):
    if not type(adaptor) in clist:
        raise ValueError(f'{type(adaptor)} not compatible with {type(me)}')

class Engine(ABC):
    @abstractmethod
    def init_engine(self):
        pass
    @abstractmethod
    def get_engine_context(self):
        pass
    @abstractmethod
    def save_object(self, database_name, table_name, partition_col=None, options=None):
        pass
    @abstractmethod
    def get_object(self, database_name, table_name, predicate=None, options=None):
        pass
    @abstractmethod
    def close_session(self):
        pass

class StorageBase(ABC):
    @abstractmethod
    def init_storage_base(self):
        pass
    @abstractmethod
    def build_storage_string(self, database, table, options=None):
        pass
    @abstractmethod
    def commit(self, database, table, options=None):
        pass
    @abstractmethod
    def close_session(self):
        pass

class MetadataProvider(ABC):
    @property
    @abstractmethod
    def adaptor_compatibility_list(self):
        pass
    
    def check_compatibility(self, adaptor):
        check_compatibility(self.adaptor_compatibility_list, adaptor, self)

    @abstractmethod
    def init_metadata_provider(self):
        pass
    @abstractmethod
    def get_database_info(self, database_name, options=None):
        pass
    @abstractmethod
    def database_exists(self, database_name, options=None):
        pass
    @abstractmethod
    def add_or_update_database(self, database_name, description=False, options=None):
        pass
    @abstractmethod
    def delete_database(self, database_name, options=None):
        pass
    @abstractmethod
    def get_table_info(self, database_name, table_name, options=None):
        pass
    @abstractmethod
    def get_dataframe(self, database_name, table_name, options=None):
        pass
    @abstractmethod
    def delete_table(self, database_name, table_name, options=None):
        pass
    @abstractmethod
    def table_exists(self, database_name, table_name, options=None):
        pass
    @abstractmethod
    def check_table_accept(self, df, database_name, table_name, partition_col, write_mode, write_format, options=None):
        pass
    @abstractmethod
    def commit_dataframe(self, df, database_name, table_name, partition_col, write_mode, write_format, options=None):
        pass
    @abstractmethod
    def close_session(self):
        pass
