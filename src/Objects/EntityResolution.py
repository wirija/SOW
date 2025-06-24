"""
Splink entity resolution
"""
from  src.Utils.DuckDB_api import duckdb_conn as dconn

def EntityResolution(
    db_name,
    table_name,
    blocking_cols, 
    compare_dict, 
):
    db = dconn(db_name=db_name)
    

    return 