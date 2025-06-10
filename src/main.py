

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
from Utils.DuckDB_api import duck_conn

def import_database(
    infile_customer = '',
    infile_transactions = '',
    db_name = ''
):
    db = duck_conn()
    db.import_from_
    return 

if __name__ == "__main__":
    
    return
