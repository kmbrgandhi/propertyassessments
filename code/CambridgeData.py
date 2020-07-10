#!/usr/bin/env python

# FULLY DEPRECATED

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cambridgema.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cambridgema.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("eey2-rv59", limit=200000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

#can export it here

"""
PLAN OF ACTION: 
Take the above data, and merge on ALL of the relevant GIS data.  Create .shp file.
- read in Excel data for given year
- Merge on 