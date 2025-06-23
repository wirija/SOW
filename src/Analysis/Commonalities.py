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
import networkx as nx
import csv

PATH_ANALYSIS_DB = r".\data\duckdb"
PATH_CONFIG_PATH = ""


class Commonalities:

    def __init__(
        self,
        db_name="staging_customers",
    ):
        self.db_name = db_name
        self.db_path = os.path.join(PATH_ANALYSIS_DB, db_name)

        # Init Database
        self.db = duckdb_conn(PATH_ANALYSIS_DB)

        # Check if Database has table customer and transactions
        self.tables = self.db.list_tables()

        self.G_static_nx = None
        self.G_static_grape = None
        self.G_trx_nx = None
        self.G_trx_grape = None

        # check tables
        req_tables = [const.TBL_CUST, const.TBL_TRX]
        for col in req_tables:
            if col not in self.tables["table_name"].values:
                raise KeyError(f"Table name '{col}' missing from {self.db_name}")

    def find_common_static_data(
        self,
        contactNumber=True,
        address=True,
        email=True,
    ):
        # Filter once for the relevant database
        filtered = self.tables[self.tables["database"] == self.db_name]

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
                raise KeyError(f"Column name '{col}' missing from {self.db_name}")

        # SQL TO RUN
        sql = (
            """WITH A AS ("""
            + " UNION ALL ".join(
                [
                    f"""
                        SELECT  DISTINCT 
                                  {const.COL_ACCOUNT_NUMBER} AS "{const.COL_ACCOUNT_NUMBER}"
                                , {const.COL_ACCOUNT_HOLDER} AS "{const.COL_ACCOUNT_HOLDER}"
                                , {col} AS "{const.COL_STATIC_DATA}"
                                , '{col}' AS "{const.COL_STATIC_DATATYPE}"
                        FROM staging_customers
                        WHERE {const.TBL_STAGING_CUSTOMER} <> ''
                        """
                    for col in required_columns[1:]
                ]
            )
            + """)"""
            + f"""CREATE OR REPLACE TABLE {const.TBL_STAGING_CUST_STATIC} AS """
            + f"""
                  "{const.COL_ACCOUNT_NUMBER}"
                , "{const.COL_ACCOUNT_HOLDER}"
                , "{const.COL_ID}"
                , "{const.COL_STATIC_DATA}" 
                , "{const.COL_STATIC_DATATYPE}"
                FROM A;"""
        )

        # Create Database
        self.db.execute_sql(sql)

        self.G_static_nx , 
        self.G_static_grape = self._build_graph(
            tbl_nodes=const.TBL_STAGING_CUST_STATIC,
            tbl_edges=const.TBL_STAGING_CUST_STATIC,
            tbl_result_nodes =  const.TBL_STAGING_STATIC_NODES,
            tbl_result_edges = const.TBL_STAGING_STATIC_EDGES,
            col_edge_src = const.COL_ID,
            col_edge_dest = const.COL_STATIC_DATA,
            col_nodes = [const.COL_ACCOUNT_NUMBER],
            col_nodes_type = [const.COL_NODE_TYPE],
        )

    def find_common_trx(
        self,
    ):
        self.G_trx_nx , 
        self.G_trx_grape = self._build_graph (
            tbl_nodes=const.TBL_STAGING_CUSTOMER,
            tbl_edges=const.TBL_STAGING_TRANSACTION,
            tbl_result_nodes =  const.TBL_STAGING_TRX_NODES,
            tbl_result_edges = const.TBL_STAGING_TRX_EDGES,
            col_edge_src = const.COL_PAYOR,
            col_edge_dest = const.COL_BENE,
            col_nodes = [const.COL_ID],
            col_nodes_type = [const.COL_NODE_TYPE],
        )
        

        


    def _build_graph(
        self,
        tbl_nodes = '',
        tbl_edges = '',
        tbl_result_nodes = '',
        tbl_result_edges = '',
        col_edge_src = '',
        col_edge_dest = '',
        col_nodes = [],
        col_nodes_type = [],
    ):

        # Build SQL Statements
        node_sql = const.SQL_GENERATE_NODES
        edge_sql = const.SQL_GENERATE_EDGES


        for node, nodetype in zip(col_nodes, col_nodes_type):
            node_sql = (
                " UNION ".join(
                    node_sql.replace("__NODE__", node)
                    .replace("__NODE_TYPE__", nodetype)
                    .replace("__TABLE__", tbl_nodes)
                    .replace("__RESULT_TABLE__", tbl_result_nodes)
                )
            ).replace("UNION CREATE OR REPLACE __RESULT_TABLE__ AS"
                        .replace("__RESULT_TABLE__", tbl_result_nodes),
                        'UNION ' ,)


        edge_sql = (
            edge_sql.replace("__NODE1__", col_edge_src)
            .replace("__NODE2__", col_edge_dest)
            .replace("__TABLE__", tbl_edges)
            .replace("__RESULT_TABLE__", tbl_result_edges)
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
                const.TBL_TRX_EDGES,
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
                const.TBL_TRX_NODES,
                csv=True,
                csv_outfile=temp_nodes_file,
            )

            ##### Grape  ########
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

            ##---------------------- 
            # NOT USED NOW
            ##---------------------- 
            # connected_components_ids = graph.get_connected_components()
            # node_type = [
            #     item.replace("'", "")
            #     for sublist in graph.get_node_type_names()
            #     for item in sublist
            # ]
            # # Assuming these are your inputs
            # node_names = list(graph.get_node_names())
            # component_ids = list(connected_components_ids[0])

            # # Zip and convert to DataFrame
            # df = pd.DataFrame(
            #     zip(
            #         node_names,
            #         node_type,
            #         component_ids,
            #     ),
            #     columns=[
            #         const.COL_NODE,
            #         const.COL_NODE_TYPE,
            #         const.COL_GROUPID,
            #     ],
            # )

            self.db.import_dataframe(
                table_name=const.TBL_GROUPTRX,
                df=df,
                replaceTable=True,
            )

            ##### NETWORK X ########
            # Load node data
            nodes_df = pd.read_csv(temp_nodes_file)

            # Load edge data
            edges_df = pd.read_csv(temp_edges_file)

            # Create a graph
            G = nx.Graph() # or nx.DiGraph() for a directed graph

            # Add nodes from the DataFrame
            # Assuming 'node_id' is the column containing node identifiers
            with open(temp_nodes_file, mode='r', newline='', encoding='utf-8',) as file:
                csv_reader = csv.DictReader(file, delimiter=const.COL_SEP, quotechar='"')
                for row in csv_reader:
                    node_id = row[const.COL_NODE]
                    attributes = {f"Type: {row[const.COL_NODE]}"}# Get all other columns as attributes
                    G.add_node(node_id, **attributes)

            # Add edges from the DataFrame
            # Assuming 'source', 'target', and 'weight' are the column names
            with open(temp_nodes_file, mode='r', newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file, delimiter=const.COL_SEP, quotechar='"')
                for row in csv_reader:
                    source = row[const.COL_SOURCE]
                    target = row[const.COL_SOURCE]
                    G.add_edge(source, target)

        return G, graph

    def _group_level_stats(
        self,
    ):
        return
