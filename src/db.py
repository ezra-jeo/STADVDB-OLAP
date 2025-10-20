import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import time

def get_engine(conn_str: str = None) -> Engine:
    """
    Create and return a SQLAlchemy engine.
    Reads connection string from environment if not passed directly.
    
    Example:
        engine = get_engine("mysql+pymysql://user:pass@localhost:3306/imdb_star")
    """
    engine = create_engine(conn_str, pool_pre_ping=True)
    return engine

def run_sql(sql: str, engine: Engine, params: dict = None) -> pd.DataFrame:
    """
    Execute a SELECT SQL query and return the result as a pandas DataFrame.
    
    Args:
        sql (str): SQL query string.
        engine (Engine): SQLAlchemy engine.
        params (dict, optional): Dictionary of bind parameters.
    
    Returns:
        pd.DataFrame: Query results.
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(sql), conn, params=params)
        return df
    except SQLAlchemyError as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()
    
def execute_sql(sql: str, engine: Engine, params: dict = None, commit: bool = True) -> None:
    """
    Execute a non-SELECT SQL statement (INSERT, UPDATE, DELETE, CREATE INDEX, etc.)
    """
    try:
        with engine.begin() as conn:  # auto-commit if successful
            conn.execute(text(sql), params or {})
        if commit:
            print("SQL executed successfully.")
    except SQLAlchemyError as e:
        print(f"Error executing statement: {e}")

def timed_query(sql: str, engine: Engine, params: dict = None) -> tuple[pd.DataFrame, float]:
    """
    Execute a query and return (DataFrame, elapsed_time_seconds)
    """
    start = time.time()
    df = run_sql(sql, engine, params)
    elapsed = time.time() - start
    print(f"Query took {elapsed:.2f} seconds.")
    return df, elapsed

