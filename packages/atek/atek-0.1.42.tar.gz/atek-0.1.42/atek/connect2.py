# %%
from pydantic.types import DirectoryPath
from sshtunnel import open_tunnel, SSHTunnelForwarder
from operator import methodcaller
import pymysql
import pandas as pd
import numpy as np
import requests
import toolz.curried as tz
from pathlib import Path
from typing import Dict, Any, Iterable, List, Callable, Type, Union
import sqlite3
from sqlite3 import Connection as SQLite
from pydantic import (
    BaseSettings,
    SecretStr,
    PositiveInt,
    FilePath,
    Field,
    DirectoryPath,
)
import logging
from atek.conversion import to_date, to_num
from atek.display import show

__all__ = [
    "Cache", "Domo", "domo", "MySQL", "mysql", "SQLite", "sqlite", "query",
]

# %%
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )


# %%
class Cache(BaseSettings):
    """Returns the paths  using the ATEK_CACHE environment variable for the module."""
    cache: DirectoryPath
    report_dir: DirectoryPath

    class Config:
        env_prefix = "ATEK_"

    @property
    def query(self) -> DirectoryPath:
        return self.cache / "query"

    @property
    def secrets(self) -> DirectoryPath:
        return self.cache / "secrets"

    @property
    def mappings(self) -> DirectoryPath:
        return self.cache / "mappings"

    @property
    def report_dir(self) -> DirectoryPath:
        return self.report_dir


    def __truediv__(self, other: Union[Path,str]):
        return Path(self.cache) / other

    def __call__(self) -> DirectoryPath:
        return self.cache

# Cache()
# Cache() / "secrets"

# %%
class Domo(BaseSettings):
    """Connection object to a DOMO instance"""
    client_id: str
    secret: SecretStr
    dataset_id: str
    _header: Dict
    _url: str
    _data: List[Dict]
    _base_url: str="https://api.domo.com/v1/datasets"

    class Config:
        underscore_attrs_are_private = True
        env_prefix = "domo_"
        env_file = Cache().query
        secrets_dir = Cache().secrets

    def __init__(self, **data) -> None:
        super().__init__(**data)
        # Authenticate
        auth_url = (
            "https://api.domo.com/oauth/token?"
            "grant_type=client_credentials&scope=data"
        )
        auth = requests.auth.HTTPBasicAuth(
            self.client_id,
            self.secret.get_secret_value()
        )
        auth_response = requests.get(auth_url, auth=auth)
        token = auth_response.json()["access_token"]
        logging.info(f"AUTHENTICATED: Domo")
        logging.debug(self)

        # Assemble post url
        self._header = {"Authorization": f"bearer {token}"}
        self.connect(self.dataset_id)

    def connect(self, dataset_id: str) -> None:
        self._url = (
            f"{self._base_url}/query/execute/{dataset_id}"
            "?includeHeaders=true"
        )

    def execute(self, sql: str, *args, **kwargs) -> pd.DataFrame:
        """Stub method to be consistant with api for SQLite() and MySQL()
        classes."""
        logging.info(f"EXECUTING: Domo Query\n{sql}")
        results = requests.post(
            self._url,
            headers=self._header,
            json={"sql": sql}
            ).json()
        columns = results["columns"]
        rows = results["rows"]
        self._data = [
            dict(zip(columns, row))
            for row in rows
        ]
        logging.info(f"RETURNED: Domo Query")

    @property
    def connection(self):
        """Stub method to be consistant with api for SQLite() and MySQL()
        classes."""
        return self

    @property
    def conn(self):
        """Stub method to be consistant with api for SQLite() and MySQL()
        classes."""
        return self

    @property
    def description(self):
        """Stub method to allow class to be used in pandas.read_sql method."""
        if len(self._data) == 0:
            return tuple()
        return tuple(
            tuple([col, type(val), None, None, None, None, None])
            for col, val in self._data[0].items()
        )

    def cursor(self):
        """Stub method to allow class to be used in pandas.read_sql method."""
        return self

    def fetchall(self) -> List[Dict]:
        """Stub method to allow class to be used in pandas.read_sql method."""
        return [row for row in self._data]

    def close(self):
        """Stub method to allow class to be used in pandas.read_sql method."""
        pass

    def __iter__(self):
        for row in self._data:
            yield row

    def datasets(self) -> pd.DataFrame:
        """Retrieves a list of datasets from the domo instance for which the
        token has access."""
        limit = 50
        offset = 0

        # Cycle through the list in chunks of 'limit'
        rows = []
        while True:
            url = f"{self._base_url}?offset={offset}&limit={limit}"
            chunk = requests.get(url, headers=self._header).json()
            if not chunk: break
            for row in chunk:
                rows.append(row)
            offset += limit
        return pd.DataFrame.from_records(rows)

    def tables(self) -> List[str]:
        return self.datasets().name.tolist()

    def col_info(self, table_name: str) -> pd.DataFrame:
        dataset_id = tz.pipe(
            self.datasets()
            .query(f"name == '{table_name}' or id == '{table_name}'")
            .id.tolist()[0]
        )
        self.connect(dataset_id)
        return tz.pipe(
            self.query("select * from table limit 1")
            .dtypes
            .to_frame(name="data_type")
            .reset_index()
            .rename(columns={"index": "column"})
            .assign(**{
                "table": table_name,
                "dataset_id": dataset_id,
                "column_index": lambda df: np.arange(len(df)),
            })
            .filter(["dataset_id", "table", "column_index", "column", "data_type"])
        )

    def schema(self) -> pd.DataFrame:
        return tz.pipe(
            self.datasets()
            .id.tolist()
            ,tz.map(self.col_info)
            ,pd.concat
        )

    def query(self, sql: str, *args, **kwargs) -> pd.DataFrame:
        self.execute(sql)
        return tz.pipe(
            pd.DataFrame.from_records(self._data)
            ,to_date("Date")
            ,to_num("Fee|Amount")
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

def domo() -> Domo:
    return Domo()

def _dict_factory(row, cursor):
    """Returns a dict object for each row of a cursor with the keys = to the
    column names"""
    return {
        col[0]: row[idx]
        for idx, col in enumerate(cursor.description)
    }


# %%
class MySQL(BaseSettings):
    """Connection object to a mysql database accessed using a jump server and
    ssh keys"""
    remote_host: str="localhost"
    remote_port: PositiveInt=3306

    jump_host: str
    jump_port: PositiveInt=22
    jump_username: str
    jump_pkey: FilePath
    jump_password: SecretStr

    server_host: str
    server_port: PositiveInt=22
    server_username: str
    server_pkey: str
    server_password: SecretStr

    db_host: str="localhost"
    db_name: str
    db_username: str
    db_password: SecretStr

    kwargs: Dict=Field(default_factory=dict)

    _jump: SSHTunnelForwarder=None
    _server: SSHTunnelForwarder=None
    _connection: pymysql.connections.Connection=None
    _with_context: bool = False
    _cursor: pymysql.cursors.Cursor

    class Config:
        underscore_attrs_are_private = True
        env_prefix = "mysql_"
        env_file = Cache().query
        secrets_dir = Cache().secrets

    def __init__(self, **data) -> None:
        super().__init__(**data)

        self._jump = open_tunnel(
            ssh_address_or_host=(self.jump_host, self.jump_port),
            remote_bind_address=(self.remote_host, self.remote_port),
            ssh_pkey=str(self.jump_pkey),
            ssh_username=self.jump_username,
            ssh_password=self.jump_password.get_secret_value(),
        )
        self._jump.start()
        logging.info(f"OPENED: {self.jump_host}:{self.jump_port}")

        self._server = open_tunnel(
            ssh_address_or_host=(self.server_host, self.server_port),
            remote_bind_address=(self.remote_host, self.remote_port),
            ssh_pkey=self.server_pkey,
            ssh_username=self.server_username,
            ssh_password=self.server_password.get_secret_value(),
        )
        self._server.start()
        logging.info(f"OPENED: {self.server_host}:{self.server_port}")

        self._connection = pymysql.connect(
            host=self.db_host,
            db=self.db_name,
            user=self.db_username,
            password=self.db_password.get_secret_value(),
            port=self._server.local_bind_port,
            **self.kwargs
        )
        logging.info(f"OPENED: {self.db_host}:{self.db_name}")

    def close(self, *args, **kwargs) -> None:
        self._connection.close(*args, **kwargs)
        # self._connection = None
        logging.info(f"CLOSED: {self.db_host}:{self.db_name}")

        self._server.stop()
        self._server = None
        logging.info(
            f"CLOSED: {self.server_host}:{self.server_port}")

        self._jump.stop()
        self._jump = None
        logging.info(f"CLOSED: {self.jump_host}:{self.jump_port}")

    @property
    def connection(self) -> pymysql.connections.Connection:
        return self._connection

    @property
    def conn(self) -> pymysql.connections.Connection:
        return self.connection

    def __enter__(self):
        self._with_context = True
        return self

    def __exit__(self, *args):
        self.close()
        self._with_context = False

    def query(self, sql: str, *args, **kwargs) -> pd.DataFrame:
        logging.info(f"EXECUTING: {self.db_host}:{self.db_name} Query\n{sql}")
        df = pd.read_sql(sql, self.conn, *args, **kwargs)
        logging.info(f"RETURNED: {self.db_host}:{self.db_name} Query")
        if not self._with_context:
            self.close()
        return df

    def col_info(self, table_name: str) -> pd.DataFrame:
        return tz.pipe(
            self.query(f"describe {table_name}")
            .assign(**{
                "table": table_name,
                "column_index": lambda df: np.arange(len(df)),
            })
            .rename(columns=lambda x: (
                "column" if x == "Field" else
                "data_type" if x == "Type" else
                "nullable" if x == "Null" else
                x.lower()
            ))
            .filter(["table", "column_index", "column", "data_type", "nullable", "key", "default", "extra"])
        )

    def tables(self) -> List[str]:
        return tz.pipe(
            self.query("show tables")
            .rename(columns=lambda x: "table_name")
            .table_name.tolist()
        )

    def schema(self) -> pd.DataFrame:
        with self as con:
            return tz.pipe(
                con.tables()
                ,tz.map(con.col_info)
                ,pd.concat
            )

    def cursor(self) -> sqlite3.Cursor:
        self._cursor = self.conn.cursor()
        return self._cursor

    def execute(self, sql: str, *args, **kwargs):
        self.cursor()
        self._cursor.execute(sql, *args, **kwargs)

    def __iter__(self):
        for row in self._cursor:
            yield _dict_factory(row, self._cursor)

def mysql() -> MySQL:
    return MySQL()


# %%
class SQLite(BaseSettings):
    """Connection object to a sqlite database"""
    path: FilePath
    kwargs: Dict=Field(default_factory=dict)
    _connection: sqlite3.Connection=None
    _with_context: bool = False
    _cursor: sqlite3.Cursor

    class Config:
        underscore_attrs_are_private = True
        env_prefix = "sqlite_"
        env_file = Cache().query
        secrets_dir = Cache().secrets

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.connect()

    def connect(self) -> sqlite3.Connection:
        self._connection = sqlite3.connect(self.path, **self.kwargs)
        logging.info(f"OPENED: {self.path}")

    def close(self) -> None:
        self._connection.close()
        # self._connection = None
        logging.info(f"CLOSED: {self.path}")

    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection

    @property
    def conn(self) -> sqlite3.Connection:
        return self.connection

    def __enter__(self):
        self._with_context = True
        return self

    def __exit__(self, *args):
        self.close()
        self._with_context = False

    def query(self, sql: str, *args, **kwargs) -> pd.DataFrame:
        logging.info(f"EXECUTING: {self.path} Query\n{sql}")
        df = pd.read_sql(sql, self.conn)
        logging.info(f"RETURNED: {self.path} Query")
        if not self._with_context:
            self.close()
        return df

    def tables(self) -> List[str]:
        return self.query("""
            select name as table_name
            from sqlite_master
            where type = 'table'
            """).table_name.tolist()

    def col_info(self, table_name: str) -> pd.DataFrame:
        if table_name not in self.tables():
            raise ValueError(f"{table_name} does not exist in {self.path}")

        self.connect()
        return tz.pipe(
            self.query(f"pragma table_info({table_name})")
            ,lambda df: df
            .assign(**{
                "table": table_name,
                "nullable": lambda df: np.where(df.notnull == 0, "YES", "NO")
            })
            .rename(columns={
                "name": "column",
                "type": "data_type",
                "cid": "column_index",
                "pk": "key",
                "dflt_value": "default",
            })
            .filter(["table", "column_index", "column", "data_type",
                "nullable", "default"])
        )

    def schema(self) -> pd.DataFrame:
        with self as con:
            return pd.concat([
                con.col_info(table)
                for table in con.tables()
            ])

    def cursor(self) -> sqlite3.Cursor:
        self.connect()
        self._cursor = self.conn.cursor()
        return self._cursor

    def execute(self, sql: str, *args, **kwargs):
        self.cursor()
        self._cursor.execute(sql, *args, **kwargs)

    def __iter__(self):
        for row in self._cursor:
            yield _dict_factory(row, self._cursor)


def sqlite() -> SQLite:
    return SQLite()

# %%
def query(connection: Union[MySQL,SQLite,Domo], sql: str, *args, **kwargs) -> List[Dict]:
    return connection.query(sql, *args, **kwargs)
