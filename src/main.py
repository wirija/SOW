

# Import databases

# DATA CLEANING PIPELINE
#   Clean Phone number  
#   Clean Address 
#   Clean Email Address

# Analytics pipeline
#   Splinkify Customers
#   Commonalities analysis
#   Remove known links

# Results
#   Some sort of confident or risk level???/
#
from Utils.DuckDB_api import duckdb_conn

def import_database(
    infile_customer = '',
    infile_transactions = '',
    db_name = ''
):
    db = duckdb_conn()
    db.import_csv("RAW_customer", infile_customer, unionByName=True )
    db.import_csv("RAW_transactions", infile_customer, unionByName=True )
    return 

if __name__ == "__main__":
    print("Hello")