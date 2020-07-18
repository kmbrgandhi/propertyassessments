import descartes, matplotlib.pyplot as plt 
import fiona
import geopandas as gpd
import pandas as pd
import censusdata
import gc
gc.collect()

fp = "/Users/kmbrgandhi/Documents/Housing/Property_Assessments/propertyassessments/ACS2018/tl_2018_25_bg/tl_2018_25_bg.shp"
acs2018sf = gpd.read_file(fp)

counties = censusdata.geographies(censusdata.censusgeo([('state', '25'), ('county', '*')]), 'acs5', 2018)

list_of_counties = []
county_data = {}
for county in counties:
    county_name = county[:-15]
    county_val = counties[county]
    county_number = county_val.geo[1][1]
    county_data[county_name] = censusdata.download('acs5', 2018,
                             censusdata.censusgeo([('state', '25'), ('county', county_number), ('block group', '*')]),
                             ['B02001_001E', 'B02001_003E', "B03003_001E", "B03003_003E", "B25003_002E", "B25003_003E", \
                             'B15003_002E', 'B15003_003E', 'B15003_004E', 'B15003_005E', 'B15003_006E', 'B15003_007E', \
                             'B15003_008E', 'B15003_009E', 'B15003_010E', 'B15003_011E', 'B15003_012E', 'B15003_013E', \
                             'B15003_014E', 'B15003_015E', 'B15003_016E', 'B15003_017E','B15003_018E', 'B15003_019E',\
                              'B15003_020E', 'B15003_021E', 'B15003_022E', 'B15003_023E','B15003_024E', 'B15003_025E'])
    # grabbing the Massachusetts data we want for each county
#B02001 is the race table: pulling black and total to form ratio
#B03001 is the hispanic table: pulling hispanic and total to form ratio
#B19013 is overall median income, Note that I could get black and white specific median incomes from B19013A and B
#B25118 is # of owner and renter occupied
#B15003 is all the education variables, going to be aggreagted later

lst_of_data = []
total = 0
for county in county_data:
    county_data[county]["county"] = county
    lst_of_data.append(county_data[county])
    total+=len(county_data[county])

final_ma = pd.concat(lst_of_data, axis=0)

# clean educational attainment
final_ma['hs'] = final_ma[['B15003_002E', 'B15003_003E', 'B15003_004E', 'B15003_005E', 'B15003_006E', 'B15003_007E', \
                             'B15003_008E', 'B15003_009E', 'B15003_010E', 'B15003_011E', 'B15003_012E', 'B15003_013E', \
                             'B15003_014E', 'B15003_015E', 'B15003_016E', 'B15003_017E', 'B15003_018E']].sum(axis=1)
final_ma['somecollege'] = final_ma[['B15003_019E', 'B15003_020E', 'B15003_021E']].sum(axis=1)
final_ma['bach'] = final_ma[['B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E']].sum(axis=1)

# drop and rename
final_ma = final_ma.drop(columns=['B15003_002E', 'B15003_003E', 'B15003_004E', 'B15003_005E', 'B15003_006E', 'B15003_007E', \
                             'B15003_008E', 'B15003_009E', 'B15003_010E', 'B15003_011E', 'B15003_012E', 'B15003_013E', \
                             'B15003_014E', 'B15003_015E', 'B15003_016E', 'B15003_017E','B15003_018E', 'B15003_019E',\
                              'B15003_020E', 'B15003_021E', 'B15003_022E', 'B15003_023E','B15003_024E', 'B15003_025E'])
final_ma = final_ma.rename(columns={'B02001_001E': "total",'B02001_003E': "black", 'B03003_001E': "total2", 'B03003_003E': "hispanic",
 'B25003_002E': "owner occupied",'B25003_003E': "renter occupied"})
assert final_ma["total"].equals(final_ma["total2"])
final_ma = final_ma.drop(columns=["total2"])

final_ma = final_ma.reset_index()

def get_value(geo, index):
    return geo.geo[index][1]

final_ma["STATEFP"] = final_ma["index"].apply(get_value, args=(0,))
final_ma["COUNTYFP"] = final_ma["index"].apply(get_value, args=(1,))
final_ma["TRACTCE"] = final_ma["index"].apply(get_value, args=(2,))
final_ma["BLKGRPCE"] =final_ma["index"].apply(get_value, args=(3,))
final_ma["GEOID"] = final_ma["STATEFP"] + final_ma["COUNTYFP"] + final_ma["TRACTCE"] + final_ma["BLKGRPCE"]
final_ma = final_ma.drop(columns=["index"])

merged_acs = acs2018sf.merge(final_ma, on="GEOID", how ="inner")
merged_acs.to_file("../cleaned/acs2018demographics.shp")