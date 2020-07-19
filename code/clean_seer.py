import numpy as np
import pandas as pd

headings = ["Year", "Postal", "state", "county", "registry", "race", "hispanic", "sex", "age", "population"]
seer = pd.read_fwf("~/Documents/Housing/Property_Assessments/propertyassessments/raw/ma.1969_2018.19ages.txt", header=None, 
	colspecs=[(0, 4), (4, 6), (6, 8), (8, 11), (11, 13), (13, 14), (14, 15), (15, 16), (16, 18), (18, 26)], names = headings)

seer.to_csv("~/Documents/Housing/Property_Assessments/propertyassessments/cleaned/ma.1969_2018.19ages.csv")





