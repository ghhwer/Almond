from .context import AlmondContext
import inspect

# Input (Represents, an input object during a tranform session)
class Input():
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name

    def get_df(self, predicate=None, options=None):
        c = AlmondContext()
        return c.get_engine().get_object(
            self.database_name, self.table_name, 
            predicate=predicate, options=options
        )

# Output (Represents, an output object during a tranform session)
class Output():
    def __init__(self, target_database, target_table):
        self.target_database = target_database
        self.target_table = target_table
   
    def as_input(self,):
        return Input(self.target_database, self.target_table)

    def write(self, df, partition_col=None, options=None):
        c = AlmondContext()
        c.get_engine().save_object(df, self.target_database, self.target_table)
        

# Decorator for a tranform session (injects input and output objects into generic transform function)
def transformation(*args, **kwargs):
    def decorator(fun):
        passed_inputs_outputs = kwargs

        def wrapper(*args, **kwargs):
            fun_expect_args = inspect.signature(fun).parameters.keys()
            overwrite = [passed_inputs_outputs[x] for x in fun_expect_args]
            return fun(*overwrite)
        return wrapper
    return decorator
