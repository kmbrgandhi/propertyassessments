import geopandas as gpd
import descartes, matplotlib.pyplot as plt 
import fiona

#for i in range(2016, 2021):


fp = "/Users/kmbrgandhi/Documents/Housing/Property_Assessments/propertyassessments/AssessingParcels2020/ASSESSING_ParcelsFY2020.shp"
parcels2020 = gpd.read_file(fp)
fp2 = "/Users/kmbrgandhi/Documents/Housing/Property_Assessments/propertyassessments/ACSData/DEMOGRAPHICS_BlockGroups2010.shp"
censusblocks2010 = gpd.read_file(fp2)
assert parcels2020.crs == censusblocks2010.crs


joined_intersect = gpd.sjoin(parcels2020, censusblocks2010, how = "left")
# drop the duplicates among any multiple intersections at random
joined_intersect_final = joined_intersect.sample(frac=1).drop_duplicates(subset = ["ML"])
