import duckdb as dd


class duckdb_conn:
    DEFAULT_DDB = r"data\duckdb\default.ddb"

    def __init__(
        self,
        db_name=None,
    ):
        self.conn = (
            dd.connect(self.DEFAULT_DDB) if db_name is None else dd.connect(db_name)
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


    def get_records(
        self,
        table_name,
        limit = 0
    ):
        sql = f"""SELECT * FROM {table_name} {"" if limit == 0 else "Limit " + str(int(limit))} """
        return self.conn.sql(sql).to_df()



    def run_sql(
        self,
        sql,
    ):
        result = self.conn.sql(sql)
        self.conn.commit()
        return result.to_df() if "SELECT" in sql.upper() else ""
