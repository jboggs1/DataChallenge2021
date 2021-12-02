import pandas as pd
import re
import math

res_data = pd.read_csv("ResidentialBoundaries.csv").to_dict(orient="row")

com_data = pd.read_csv("CommercialBoundaries.csv").to_dict(orient="row")

trans_data = pd.read_csv("Transportation.csv").to_dict(orient="row")

park_data = pd.read_csv("parking.csv").to_dict(orient="row")


res_bounds = []
for i in range(1, 18):
    poly = []
    j = 0
    while j < 57 and math.isnan(res_data[j]["Res" + str(i) + "_Lat"]) == False:
        pair = []
        pair.append(res_data[j]["Res" + str(i) + "_Long"])
        pair.append(res_data[j]["Res" + str(i) + "_Lat"])
        poly.append(pair)
        j = j + 1
        #print("j: " + str(j) + " i: " + str(i))
    res_bounds.append(poly)
    
com_bounds = []
for i in range(1, 7):
    poly = []
    j = 0
    while j < 37 and math.isnan(com_data[j]["Com" + str(i) + "_Lat"]) == False:
        pair = []
        pair.append(com_data[j]["Com" + str(i) + "_Long"])
        pair.append(com_data[j]["Com" + str(i) + "_Lat"])
        poly.append(pair)
        j = j + 1
        #print("j: " + str(j) + " i: " + str(i))
    com_bounds.append(poly)
    
trans_points = []
for i in range(261):
    pair = []
    pair.append(trans_data[i]["X"])
    pair.append(trans_data[i]["Y"])
    trans_points.append(pair)

park_points = []
for i in range(27):
    pair = []
    pair.append(park_data[i]["LONG"])
    pair.append(park_data[i]["LAT"])
    park_points.append(pair)