

import requests
import pandas as pd
from DuckDB_api import duckdb_conn 
import time
import pandas as pd
import requests
import time
from joblib import Parallel, delayed
import os



# Assuming DEBUGMODE is defined elsewhere, e.g., DEBUGMODE = False
DEBUGMODE = False

# This function defines what happens for *each* item (a single 'postal' code)
# from the range you want to parallelize.
def process_postal_code(postal):
    """
    Processes a single postal code to fetch data from the OneMap API.
    Returns a DataFrame containing the results for the given postal code.
    """
    print(f"Processing - {postal}")
    i = 1
    totalNumPages = 1
    postal_df = pd.DataFrame()

    while i <= totalNumPages:
        url = rf"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={str(postal)}&returnGeom=Y&getAddrDetails=Y&pageNum={i}"
        
        try:
            r = requests.get(url)
            r.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            data = r.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for postal code {postal}, page {i}: {e}")
            break

        results = data.get("results", [])
        if results:
            postal_df = pd.concat([postal_df, pd.DataFrame(results)]).reset_index(drop=True)
        
        totalNumPages = data.get("totalNumPages", 0)
        print(f"Postal {postal} - Page {i} / {totalNumPages}")
        i += 1
        
        if (i - 1) % 10000 == 0 and i > 1:
            print(f"Pausing for 0.5 seconds after processing 10000 pages for postal {postal}...")
            time.sleep(0.5)

        if DEBUGMODE:
            print(data)
            print(totalNumPages)
            print(postal_df)
            
    return postal_df

if __name__ == '__main__':
    num_cores = os.cpu_count()
    print(f"Using {num_cores} CPU cores for parallel processing.")

    itt = 111111
    end = 222222
    real_end = 999999

    for item in range(1, 10, 1):
        print (item)

        # This is your range for the loop:
        postal_codes_to_process = range(itt*item, itt*(item+1), 1)

        # This line is the heart of parallelizing your 'for' loop.
        # It takes each 'postal' value from 'postal_codes_to_process'
        # and submits it as a separate job to be run by 'process_postal_code'
        # in parallel.
        results_list = Parallel(n_jobs=num_cores, verbose=10)(
            delayed(process_postal_code)(postal) for postal in postal_codes_to_process
        )

        # After all parallel jobs are done, concatenate their results
        df = pd.concat(results_list, ignore_index=True)

        df.to_excel("onemapApi.xlsx")
        db = duckdb_conn("onemapApi.ddb")
        db.import_dataframe(f"RAW_onemap_{item}", df, replaceTable=True,)


        print("\nProcessing complete!")
