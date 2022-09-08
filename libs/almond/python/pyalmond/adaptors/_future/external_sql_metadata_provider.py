from sqlalchemy.orm import (
    declarative_base, relationship,
    Session
)
from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    create_engine, select, update
)
import json

Base = declarative_base()

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

class Database(Base):
    __tablename__ = 'database'

    name = Column(String, primary_key=True)
    description = Column(String)

    def __repr__(self):
        return f"database(name={self.name!r}, description={self.description!r})"
    
class Table(Base):
    __tablename__ = 'table'

    table_name = Column(String, primary_key=True)
    database_name = Column(String, ForeignKey('database.name'))
    schema_json = Column(String, nullable=False)
    partitions_json = Column(String, nullable=True)

    def __repr__(self):
        return f"database(table_name={self.table_name!r}, database_name={self.database_name!r}, description={self.description!r})"

class LocalMetadataSqlite():#MetadataProvider):
    def __init__(self, filename='./almond_local_metadata.sqlite'):
        self.filename=filename
        self.engine = create_engine(f"sqlite+pysqlite:///{self.filename}", echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def __fetch_database(self, database_name):
        k = self.session.execute(
            select(Database).where(Database.name == database_name)
        ).first()
        if k == None: return k
        else: return k[0]

    def __fetch_table(self, database_name, table_name):
        k = self.session.execute(
            select(Table).where(Table.database_name == database_name, Table.table_name == table_name)
        ).first()
        if k == None: return k
        else: return k[0]

    def database_exists(self, database_name):
        return (self.__fetch_database(database_name) is not None)
    
    def table_exists(self, database_name, table_name):
        return (self.__fetch_table(database_name, table_name) is not None)

    def add_or_update_database(self, database_name, description=None):
        if(self.database_exists(database_name)):
            self.session.execute(
                update(Database).where(Database.name == database_name).values(description=description)
            )
            self.session.commit()
        else:
            db = Database(name=database_name, description=description)
            self.session.add(db)
            self.session.commit()

    def check_table_accept(self, df, database_name, table_name, partition_col, write_mode):
        # First we check if table exists
        if self.database_exists(database_name):
            if self.table_exists(database_name, table_name):
                tb = self.__fetch_database(database_name, table_name)
                # Stored info
                df_stored_schema = json.loads(tb.schema_json)
                df_stored_part_json = json.loads(tb.partitions_json)
                # DF info
                df_schema = json.loads(schema)
                schema_match = (ordered(df_schema) == ordered(stored_schema))
                parti_col_match = (ordered(partition_col) == ordered(df_stored_part_json))
                if( schema_match and parti_col_match ):
                    return True
                else:
                    raise ValueError(f'Dataframe does not match stored info: schema_match={schema_match} parti_col_match={parti_col_match}')
            else:
                return True
        else:
            raise ValueError(f'Database {database_name} does not exist!')
    def commit_dataframe(self, )