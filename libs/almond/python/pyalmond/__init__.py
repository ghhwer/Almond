import yaml
import importlib
import logging
from Almond.context import AlmondContext
import traceback

def instanciate_by_yaml(yaml, key):
    class_path = yaml[key].get('instance')
    args = yaml[key].get('args', [])
    kwargs = yaml[key].get('kwargs', {})
    
    import_path = '.'.join(class_path.split('.')[:-1])
    class_name = class_path.split('.')[-1]
    i = importlib.import_module(import_path)
    instance = getattr(i, class_name)(*args, **kwargs)
    return instance

def init_ctx_by_config(config_yaml):
    logging.info(f'Starting AlmondContext from file: {config_yaml}')

    with open(config_yaml) as file:
        context_conf = yaml.load(file, Loader=yaml.FullLoader)

    engine = instanciate_by_yaml(context_conf, 'Engine')
    storage_base = instanciate_by_yaml(context_conf, 'StorageBase')
    metadata = instanciate_by_yaml(context_conf, 'Metadata')

    ctx = AlmondContext()
    ctx.register(engine, storage_base, metadata)
    ctx.init()
    
    logging.info(f'Loaded engine: {ctx.get_engine().__class__}')
    logging.info(f'Loaded storage base: {ctx.get_storage_base().__class__}')
    logging.info(f'Loaded metadata provider: {ctx.get_metadata().__class__}')

    return ctx

class AlmondSession:
    def __init__(self, config_file):
        self.config_file = config_file
        self.ctx = init_ctx_by_config(self.config_file)

    def get_ctx(self):
        return self.ctx

    def close(self):
        self.ctx.close_session()

    def __enter__(self):
        return self.ctx
  
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            self.close()
            return False
        self.close()
        return True