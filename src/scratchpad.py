from Utils.DuckDB_api import duckdb_conn
import pandas as pd


db = duckdb_conn()


df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})


db.import_dataframe(df=df, table_name="test_df", replaceTable=True)

print(db.get_records("test_df"))