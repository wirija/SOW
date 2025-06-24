import duckdb as dd
import os


class duckdb_conn:
    DEFAULT_DDB = r"default.ddb"
    DEFAULT_PATH = r"data\duckdb"
    
    def __init__(
        self,
        db_name=r"default.ddb",
        db_path=r"data\duckdb"
    ):
        self.dbName = db_name
        self.db_path = db_path
        self.db_FullPath = os.path.join(db_path, db_name)
        self.conn = (
            dd.connect(self.db_FullPath)
        )
        return

    def import_csv(
        self,
        table_name,
        inPath,
        unionByName=True,
        replaceTable = False,
    ):
        inPath = inPath + rf"\*.csv"
        sql = f"""
                CREATE {"OR REPLACE" if replaceTable else ""} TABLE {table_name}
                SELECT  *
                FROM    read_csv(
                                      {inPath}
                                    , sep = ',' 
                                    , delim = '"'
                                    , UNION_BY_NAME = {unionByName}
                                    , header=True
                                )
                """

        self.conn.execute(sql)
        self.conn.commit()

    def import_dataframe(
        self,
        table_name,
        df,
        replaceTable=False,
    ):
        self.conn.register('my_df', df)
        sql = f"""CREATE {'OR REPLACE' if replaceTable else ''} TABLE {table_name} AS SELECT * FROM my_df"""
        self.conn.execute(sql)
        return


    def list_tables (
        self,
        schema = '',
    ):
        tables = self.conn.sql("""SHOW ALL TABLES;""").to_df()
        return tables[ tables['database'] == self.db_FullPath ] 
    

    def get_records(
        self,
        table_name,
        limit = 0, 
        columns = [],
        csv = False,
        csv_outfile = '',
        csv_delim = '|',
        csv_quote = '"',
        csv_header = True,

    ):
        # if outfile is missing - assume it is just a record pull
        if csv and (csv_outfile == '' or not os.access(csv_outfile, os.W_OK)):
            csv = False

        columns = (
            ', '.join(f'"{col}"' for col in columns)
            if columns
            else '*'
        )

        sql = f"""SELECT {columns} FROM {table_name} {"" if limit == 0 else "Limit " + str(int(limit))} """
        if csv:
            sql = """COPY (""" + sql + f""" ) TO '{csv_outfile}' (HEADER = {str(csv_header).lower()}, DELIM = {csv_delim}, QUOTE = {csv_quote});"""

        result = self.conn.sql(sql)
        self.conn.commit()
        
        return result.to_df() if csv == False else True
    

    def create_table_class (
      self,
      cls      
    ):
        create_stt = SQLTableGenerator(cls)
        self.execute_sql(create_stt)

        

    def execute_sql(
        self,
        sql,
    ):
        self.conn.sql(sql)
        self.conn.commit()
        return True



class SQLTableGenerator:
    python_to_sql = {
        str: "VARCHAR(255)",
        int: "INTEGER",
        float: "REAL",
        bool: "BOOLEAN",
    }

    def __init__(self, cls):
        self.cls = cls
        self.table_name = cls.__name__

    def get_fields(self):
        instance = self.cls()
        return {
            key: type(value)
            for key, value in vars(instance).items()
        }

    def generate_create_table(self):
        fields = self.get_fields()
        sql_fields = []

        for name, py_type in fields.items():
            sql_type = self.python_to_sql.get(py_type, "TEXT")
            sql_fields.append(f"    {name} {sql_type}")

        fields_sql = ",\n".join(sql_fields)
        return f"CREATE TABLE {self.table_name} (\n{fields_sql}\n);"