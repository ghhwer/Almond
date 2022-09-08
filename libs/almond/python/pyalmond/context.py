class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class AlmondContext(metaclass=SingletonMeta):
    def register(
        self, engine, storage_base, metadata_provider
    ):
        self.__engine = engine
        self.__storage_base = storage_base
        self.__metadata_provider = metadata_provider

        # Checking Compatibility
        self.__metadata_provider.check_compatibility(self.__storage_base)
        self.__metadata_provider.check_compatibility(self.__engine)
        
        self.__configs = {}
        self.__is_registred = True
    
    def init(self,):
        # Init in order
        self.__storage_base.init_storage_base()
        self.__metadata_provider.init_metadata_provider()
        self.__engine.init_engine()
    
    def close_session(self,):
        # Init in order
        self.__storage_base.close_session()
        self.__metadata_provider.close_session()
        self.__engine.close_session()

    def is_registred(self):
        try:
            return self.__is_registred
        except:
            return False
    
    def __test_context_ready(self):
        if(not self.is_registred()):
            raise EnvironmentError("AlmondContext is not registred yet")

    def set_config(self, config_name, config_value):
        self.__test_context_ready()
        current_config_value = self.__configs.get(config_name, None)
        if(type(config_value) == dict and type(current_config_value) == dict):
            self.__configs[config_name].update(config_value)
        if(type(config_value) == list and type(current_config_value) == list):
            self.__configs[config_name] + config_value
        if(type(current_config_value) == list):
            self.__configs[config_name].append(config_value)
        else:
            self.__configs[config_name] = config_value

    def get_config(self, config_name):
        self.__test_context_ready()
        return self.__configs.get(config_name, None)
    
    def get_storage_base(self):
        self.__test_context_ready()
        return self.__storage_base
    
    def get_engine(self):
        self.__test_context_ready()
        return self.__engine
    
    def get_metadata(self):
        self.__test_context_ready()
        return self.__metadata_provider