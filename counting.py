import pandas as pd
import re

data = pd.read_csv("data_table.csv").to_dict(orient="row")


num2020 = 0
for i in range(len(data)):
    if data[i]["SDate"][-4:] == "2020":
        num2020 += 1

num2019 = 0
for i in range(len(data)):
    if data[i]["SDate"][-4:] == "2019":
        num2019 += 1

total = 0
for i in range(len(data)):
    if data[i]["START ON CAMPUS"] == "Yes" and data[i]["END ON CAMPUS"] == " Yes" and data[i]["SDate"][-4:] == "2019":
        total += 1
