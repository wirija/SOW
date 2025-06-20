# Database tables
TBL_GROUPSTATIC = "results_customer_groups_static"
TBL_GROUPTRX = "results_customer_groups_trx"
TBL_GROUPSTATS = "results_group_stats"
TBL_NODES = 'graph_Nodes'
TBL_EDGES = 'graph_Edges'
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
COL_CONTACT_NUMBER = 'contact number'
COL_ADDRESS = "address"
COL_EMAIL = "email"

COL_SEP = "|"

# SQL Statments??
SQL_GENERATE_NODES = (
f"""
CREATE OR REPLACE __RESULT_TABLE__ AS 
SELECT DISTINCT __NODE1__ AS "{COL_NODE}", CONCAT(__NODE1_TYPE__, '|') AS "{COL_NODE_TYPE}"
FROM __TABLE__
UNION
SELECT DISTINCT __NODE2__ AS "{COL_NODE}" ,  CONCAT(__NODE2_TYPE__, '|') AS "{COL_NODE_TYPE}"
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