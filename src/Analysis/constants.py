# Database tables
TBL_STAGING_CUSTOMER = '_staging_customer'
TBL_STAGING_TRANSACTION = '_staging_transaction'

TBL_STAGING_CUST_STATIC = '_staging_cust_static_data'
TBL_STAGING_STATIC_NODES = "_staging_static_nodes"
TBL_STAGING_STATIC_EDGES = "_staging_static_edges"

TBL_STAGING_TRX_NODES = "_staging_cust_trx_nodes"
TBL_STAGING_TRX_EDGES = "_staging_cust_trx_edges"

TBL_RESULT_GROUP_STATIC = "_result_cust_group_static"
TBL_RESULT_GROUP_TRX = "_result_group_trx"
TBL_TRX_NODES = 'graph_trx_Nodes'
TBL_TRX_EDGES = 'graph_trx_edges'
TBL_CUST  = 'customers'
TBL_TRX = 'transactions'

# Database columns
COL_PAYOR = 'payor'
COL_PAYOR_TYPE = 'payor type'
COL_BENE = 'beneficiary'
COL_BENE_TYPE = 'beneficiary type'
COL_SOURCE  = 'source'
COL_DEST =  'destination'
COL_DATE = 'date'
COL_CURR = 'currency'
COL_AMT = 'amount'
COL_LOCAL_CURR = 'local currency'
COL_LOCAL_AMT = 'local amount'
COL_NODE = 'node'
COL_NODE_TYPE = 'node type'
COL_GROUPID = 'group ID'
COL_FUND_IN_TOTAL = 'fund in - total'
COL_FUND_IN_DAYS = 'fund in - days'
COL_FUND_OUT_TOTAL = 'fund out - total'
COL_FUND_OUT_DAYS = 'fund out - days'
COL_ID = "ID"
COL_GROUP_ID = "ID"
COL_ACCOUNT_NUMBER = 'account number'
COL_ACCOUNT_HOLDER = 'account holder'
COL_CONTACT_NUMBER = 'contact number'
COL_ADDRESS = "address"
COL_EMAIL = "email"
COL_STATIC_DATA = "static data"
COL_STATIC_DATATYPE = "static data type"

COL_SEP = "|"

# SQL Statments??
SQL_GENERATE_NODES = (
f"""
CREATE OR REPLACE __RESULT_TABLE__ AS 
SELECT DISTINCT __NODE__ AS "{COL_NODE}", CONCAT(__NODE_TYPE__, '|') AS "{COL_NODE_TYPE}"
FROM __TABLE__
"""
)


SQL_GENERATE_EDGES = (
f"""
CREATE OR REPLACE __RESULT_TABLE__ AS 
SELECT DISTINCT __NODE1__ AS "{COL_SOURCE}" , CONCAT(__NODE2__, '|') AS "{COL_DEST}"
FROM __TABLE__
"""
)


SQL_GENERATE_GROUP_TABLE = (
"""
CREATE OR REPLACE __RESULT_TABLE__ AS 
SELECT *
FROM __TABLE__
"""
)