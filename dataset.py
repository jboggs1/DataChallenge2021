import pandas as pd
import re

data = pd.read_csv("Data_Lv3_UMDOTS_Escooters_edited.csv").to_dict(orient="row")

for i in range(len(data)):
     temp_path = re.sub("\s", "", data[i]["PATH"])
     temp_path = re.findall("\[-?[0-9]+\.[0-9]+,-?[0-9]+\.[0-9]+\]", temp_path)
     temp_timestamp = re.sub("\s", "", data[i]["TIMESTAMPS"])
     new_timestamp = re.findall("[0-9]+-[0-9]+-[0-9]+T[0-9]+:[0-9]+:[0-9]+Z", temp_timestamp)
     new_path = []
     for j in range(len(temp_path)):
         coords = re.findall("-?[0-9]+\.[0-9]+", temp_path[j])
         for k in range(len(coords)):
             coords[k] = float(coords[k])
         new_path.append(coords)
     data[i]["PATH"] = new_path
     data[i]["TIMESTAMPS"] = new_timestamp
     
    
# temp = re.sub("\s", "", data[0]["PATH"])
# temp = re.findall("\[-?[0-9]+\.[0-9]+,-?[0-9]+\.[0-9]+\]", temp)
# temp = re.findall("-?[0-9]+\.[0-9]+", temp[0])

# temp = re.sub("\s", "", data[0]["TIMESTAMPS"])
# temp = re.findall("[0-9]+-[0-9]+-[0-9]+T[0-9]+:[0-9]+:[0-9]+Z", temp)


def save_path(num, ends = False):
    lon = []
    lat = []
    f = open("path" + str(num) + ".kml","w+")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    f.write("<kml xmlns=\"http://earth.google.com/kml/2.0\">")
    f.write("<Document>")
    if ends == True:
        f.write("<Placemark>")
        f.write("<name>" + str("start") + "</name>")
        f.write("<Point><coordinates>" + str(data[num]["START LONG"]) + "," + str(data[num]["START LAT"]) + ",0</coordinates></Point>")
        f.write("</Placemark>")
    for i in range(len(data[num]["PATH"])):
        lon.append(float(data[num]["PATH"][i][0]))
        lat.append(float(data[num]["PATH"][i][1]))
        test = {"Longitude": lon, "Latitude": lat}
        f.write("<Placemark>")
        f.write("<name>" + str(i) + "</name>")
        f.write("<Point><coordinates>" + str(data[num]["PATH"][i][0]) + "," + str(data[num]["PATH"][i][1]) + ",0</coordinates></Point>")
        f.write("</Placemark>")
    if ends == True:
        f.write("<Placemark>")
        f.write("<name>" + str("end") + "</name>")
        f.write("<Point><coordinates>" + str(data[num]["END LONG"]) + "," + str(data[num]["END LAT"]) + ",0</coordinates></Point>")
        f.write("</Placemark>")
    f.write("</Document>")
    f.write("</kml>")
    f.close
    

    #df = pd.DataFrame(test)  
    
    # saving the dataframe  
    #df.to_csv('b.csv') 