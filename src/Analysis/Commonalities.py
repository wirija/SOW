import networkx

"""
    Static Data
    [X] Address
    [X] Phone Number   
    [X] Emails
    
    Transactional Data
    [ ] Address
    [ ] CounterpartyName
    [ ] Contact Number
    [ ] is Corp Service provider

    Corporate Ownership
    [ ] Parse into Table

    Analysis
    [X] Commonality Analysis - Static
    [X] Commonality Analysis - Transaction
"""
from src.Utils.DuckDB_api import duckdb_conn
import src.Analysis.constants as const
import os
import tempfile
import grape
from grape import Graph
import pandas as pd

PATH_ANALYSIS_DB = r".\data\duckdb"
PATH_CONFIG_PATH = ""


class Commonalities:

    def __init__(
        self,
        DBname="staging_customers",
    ):
        self.DBName = DBname
        self.DBpath = os.path.join(PATH_ANALYSIS_DB, DBname)

        # Init Database
        self.db = duckdb_conn(PATH_ANALYSIS_DB)

        # Check if Database has table customer and transactions
        self.tables = self.db.list_tables()

        self.graph_trx = None

        # check tables
        req_tables = [const.TBL_CUST, const.TBL_TRX]
        for col in req_tables:
            if col not in self.tables["table_name"].values:
                raise KeyError(f"Table name '{col}' missing from {self.DBName}")

    def find_common_static_data(
        self,
        contactNumber=True,
        address=True,
        email=True,
    ):
        # Filter once for the relevant database
        filtered = self.tables[self.tables["database"] == self.DBName]

        # Required columns to check
        required_columns = ["ID"] + [
            col
            for col, flag in {
                const.COL_CONTACT_NUMBER: contactNumber,
                const.COL_ADDRESS: address,
                const.COL_Email: email,
            }.items()
            if flag
        ]

        if len(required_columns) < 2:
            raise ValueError("Grouping should be based on at least 1 column")
        # Check for missing columns
        for col in required_columns:
            if col not in filtered["column_name"].values:
                raise KeyError(f"Column name '{col}' missing from {self.DBName}")

        # SQL TO RUN
        sql = (
            """WITH A AS ("""
            + " UNION ALL ".join(
                [
                    f"""
                        SELECT  DISTINCT 
                                  ID
                                , {col} AS "Static Data"
                                , '{col}' AS "Static Data Type"
                        FROM staging_customers
                        WHERE {col} <> ''
                        """
                    for col in required_columns[1:]
                ]
            )
            + """)"""
            + f"""CREATE OR REPLACE TABLE {const.TBL_GROUPSTATIC} AS """
            + """SELECT ROW_NUMBER() OVER () AS "Group ID", 
                , "ID"
                , "Static Data" 
                , "Static Data Type"
                FROM A;"""
        )

        # Create Database
        self.db.execute_sql(sql)

        # combine by the various items
        for col in required_columns[1:]:
            sql = f"""
                        WITH cte_group AS (
                            SELECT    MIN(ID) AS "ID"
                                    , "Static Data"
                            FROM    {const.TBL_GROUPSTATIC}
                            WHERE   "Static Data Type" = '{col}'
                            GROUP BY "Static Data"
                        )
                        UPDATE  {const.TBL_GROUPSTATIC}
                        SET     ID = cte_group.ID
                        FROM    cte_group
                        WHERE   {const.TBL_GROUPSTATIC}."Static Data" = 
                                cte_group."Static Data";
                    """
            self.db.execute_sql(sql)

    def find_common_bene_payor(
        self,
        Internal=True,
        External=True,
        Both=True,
    ):

        # Build SQL Statements
        node_sql = const.SQL_GENERATE_NODES
        edge_sql = const.SQL_GENERATE_EDGES

        edge_sql = (
            edge_sql.replace("__NODE1__", const.COL_BENE)
            .replace("__NODE2__", const.COL_PAYOR)
            .replace("__TABLE__", const.TBL_TRX)
            .replace("__RESULT_TABLE__", const.TBL_EDGES)
        )

        node_sql = (
            node_sql.replace("__NODE1__", const.COL_BENE)
            .replace("__NODE2__", const.COL_PAYOR)
            .replace("__NODE1_TYPE__", const.COL_BENE_TYPE)
            .replace("__NODE2_TYPE__", const.COL_PAYOR_TYPE)
            .replace("__TABLE__", const.TBL_TRX)
            .replace("__RESULT_TABLE__", const.TBL_NODES)
        )

        # run sql
        self.db.execute_sql(edge_sql)
        self.db.execute_sql(node_sql)

        graph = grape.Graph()
        # write to tempdirectory
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create a file inside the temporary directory
            temp_edges_file = os.path.join(
                tmpdirname,
                "edges.csv",
            )
            self.db.get_records(
                const.TBL_EDGES,
                csv=True,
                csv_outfile=temp_edges_file,
                csv_delim="|",
                csv_quote="",
            )

            temp_nodes_file = os.path.join(
                tmpdirname,
                "nodes.csv",
            )
            self.db.get_records(
                const.TBL_NODES,
                csv=True,
                csv_outfile=temp_nodes_file,
            )
            graph = Graph.from_csv(
                node_path=temp_nodes_file,
                nodes_column=const.COL_NODE,
                node_list_node_types_column=const.COL_NODE_TYPE,
                node_list_separator=const.COL_SEP,
                edge_path=temp_edges_file,
                sources_column=const.COL_SOURCE,
                destinations_column=const.COL_DEST,
                edge_list_separator=const.COL_SEP,
                directed=False,
                name="Group Graph",
            )

            connected_components_ids = graph.get_connected_components()
            node_type = [
                item.replace("'", "")
                for sublist in graph.get_node_type_names()
                for item in sublist
            ]
            # Assuming these are your inputs
            node_names = list(graph.get_node_names())
            component_ids = list(connected_components_ids[0])

            # Zip and convert to DataFrame
            df = pd.DataFrame(
                zip(
                    node_names,
                    node_type,
                    component_ids,
                ),
                columns=[
                    const.COL_NODE,
                    const.COL_NODE_TYPE,
                    const.COL_GROUPID,
                ],
            )

            self.db.import_dataframe(
                table_name=const.TBL_GROUPTRX,
                df=df,
                replaceTable=True,
            )

            self.graph_trx = graph

    def _group_level_stats(
        self,
    ):
        return
