import pandas as pd
import numpy as np
import matplotlib.path as mpltPath
import copy
import math
import os
import numpy as np
from PIL import ImageTk, Image
from PIL import ImageDraw

top = 39.00753
bottom = 38.98097
left = -76.96197
right = -76.9309

# # regular polygon for testing
# lenpoly = 100
# polygon = [[np.sin(x)+0.5,np.cos(x)+0.5] for x in np.linspace(0,2*np.pi,lenpoly)[:-1]]
# 
# # random points set of points to test 
# N = 10000
# points = np.random.rand(N,2)
# 
# # Matplotlib mplPath
# path = mpltPath.Path(polygon)
# inside2 = path.contains_points(points)
# 
whole = []
for i in range(40325):
    whole.append(i)

data2 = pd.read_csv("Oncampus_Boundary2.csv").to_dict(orient="row")

boundry = []
for i in range(len(data2)):
    pair = []
    pair.append(data2[i]["Longitude"])
    pair.append(data2[i]["Latitude"])
    boundry.append(pair)
    

path = mpltPath.Path(boundry) 
#inside = path.contains_points(data[1]["PATH"])

def rides_from_year(data, year):
    indexes = []
    for i in range(len(data)):
        if data[i]["START"][0:4] == str(year) and data[i]["VEHICLE_TYPE"] == 'Scooter':
            indexes.append(i)
    return indexes
    
    
def get_starts(data, indexes):
    pairs = []
    for i in range(len(indexes)):
        temp = []
        temp.append(data[indexes[i]]["START LONG"])
        temp.append(data[indexes[i]]["START LAT"])
        pairs.append(temp)
    return pairs
    
def get_ends(data, indexes):
    pairs = []
    for i in range(len(indexes)):
        temp = []
        temp.append(data[indexes[i]]["END LONG"])
        temp.append(data[indexes[i]]["END LAT"])
        pairs.append(temp)
    return pairs
    
def endpoint_locations(starts, ends):
    pairs = []
    starts_bools = path.contains_points(starts)
    ends_bools = path.contains_points(ends)
    for i in range(len(starts)):
        temp = []
        temp.append(starts_bools[i])
        temp.append(ends_bools[i])
        pairs.append(temp)
    return pairs
    
def get_endpoint_indexes(endpoints, index, start, end):
    indexes = []
    for i in range(len(endpoints)):
        if endpoints[i][0] == start and endpoints[i][1] == end:
            indexes.append(index[i])
    return indexes
    
def find_exit_points(data, indexes):
    points = []
    for i in range(len(indexes)):
        bools = path.contains_points(data[indexes[i]]["PATH"])
        broken = False
        for j in range(len(bools)):
            if bools[j] == False:
                points.append(data[indexes[i]]["PATH"][j-1])
                broken = True
                break
        #if broken == False:
            #points.append(data[indexes[i]]["PATH"][len(data[indexes[i]]["PATH"]) - 1])
    return points   
    
def find_entrance_points(data, indexes):
    points = []
    for i in range(len(indexes)):
        bools = path.contains_points(data[indexes[i]]["PATH"])
        broken = False
        for j in range(len(bools)):
            if bools[j] == True:
                points.append(data[indexes[i]]["PATH"][j-1])
                broken = True
                break
        #if broken == False:
            #points.append(data[indexes[i]]["PATH"][len(data[indexes[i]]["PATH"]) - 1])
    return points  
                
def save_points(pairs, index, name, data_name="Index"):
    f = open(name + ".kml","w+")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    f.write("<kml xmlns=\"http://earth.google.com/kml/2.0\">")
    f.write("<Document>")
    for i in range(len(pairs)):
        #if index[i] > 1:
        f.write("<Placemark>")
        f.write("<name>" + str(index[i]) + "</name>")
        f.write("<ExtendedData><SchemaData schemaUrl=\"#test\">")
        f.write("<SimpleData name=\"" + data_name + "\">" + str(index[i]) + "</SimpleData>")
        f.write("</SchemaData></ExtendedData>")
        f.write("<Point><coordinates>" + str(pairs[i][0]) + "," + str(pairs[i][1]) + ",0</coordinates></Point>")
        f.write("</Placemark>")
    f.write("</Document>")
    f.write("</kml>")
    f.close
    
def average_distance(data, index):
    total = 0
    maximum = 0
    for i in range(len(index)):
        if data[index[i]]["DISTANCE"] > 0 and data[index[i]]["DISTANCE"] < 25 and data[index[i]]["MINUTES"] > 0 and data[index[i]]["MINUTES"] < 120:
            if data[index[i]]["DISTANCE"] > maximum:
                maximum = data[index[i]]["DISTANCE"]
            total += data[index[i]]["DISTANCE"]
    print(maximum)
    return total/len(index)
    
def get_exit_indexes(data, year):
    index = rides_from_year(data, str(year))
    
    starts = get_starts(data, index)
    ends = get_ends(data, index)
    bools = endpoint_locations(starts, ends)
    return get_endpoint_indexes(bools, index, True, False)
    
def get_entrance_indexes(data, year):
    index = rides_from_year(data, str(year))
    
    starts = get_starts(data, index)
    ends = get_ends(data, index)
    bools = endpoint_locations(starts, ends)
    return get_endpoint_indexes(bools, index, False, True)
    
def get_destination_info(data, index, res, com, trans, radius=1):
    dests_count = {"res": 0, "com": 0, "trans": 0}
    dests = []
    for i in range(len(index)):
        point = [data[index[i]]["END LONG"], data[index[i]]["END LAT"]]
        dest = []
        for j in range(len(res)):
            path = mpltPath.Path(res[j])
            if path.contains_point(point):
                dest.append("Yes")
                dests_count["res"] += 1
                #print(res[j])
                break
        if len(dest) == 0:
            dest.append("No")
        for j in range(len(com)):
            path = mpltPath.Path(com[j])
            if path.contains_point(point):
                dest.append("Yes")
                dests_count["com"] += 1
                break
        if len(dest) == 1:
            dest.append("No")
        for j in range(len(trans)):
            if (((point[0] - trans[j][0]) ** 2) + ((point[1] - trans[j][1]) ** 2)) ** (0.5) < 0.0001373626373626374:
                dest.append("Yes")
                dests_count["trans"] += 1
                break
        if len(dest) == 2:
            dest.append("No")
        dests.append(dest)
    return dests, dests_count
        
        
def percent_in_parking(ends, parking):
    total = 0
    for i in range(len(ends)):
        for j in range(len(parking)):
            if (((ends[i][0] - parking[j][0]) ** 2) + ((ends[i][1] - parking[j][1]) ** 2)) ** (0.5) < 0.0001373626373626374*2:
                total += 1
                break
    print(total)
    return total/len(ends)
     
def save_destinations(dests):
    f = open("dests" + ".csv","w+")
    f.write("RESIDENTIAL,COMMERCIAL,TRANSPORTATION\n")
    for i in range(len(dests)):
        f.write(dests[i][0] + "," + dests[i][1] + "," + dests[i][2] + "\n")
    f.close()
              
def save_starts_ends(data):
    index = []
    for i in range(len(data)):
        index.append(i)
    starts = get_starts(data, index)
    ends = get_ends(data, index)
    bools = endpoint_locations(starts, ends)
    
    f = open("start_end" + ".csv","w+")
    f.write("START ON CAMPUS,END ON CAMPUS\n")
    for i in range(len(bools)):
        if bools[i][0] == True:
            f.write("Yes,")
        else:
            f.write("No,")
        if bools[i][1] == True:
            f.write("Yes\n")
        else:
            f.write("No\n")
    f.close()
    
def get_clusters(points):
    clusters = []
    totals = []
    counts = []
    for i in range(len(points)):
        added = False
        for j in range(len(clusters)):
            if (((points[i][0] - clusters[j][0]) ** 2) + ((points[i][1] - clusters[j][1]) ** 2)) ** (0.5) < 0.0001373626373626374*3:
                counts[j] += 1
                totals[j][0] += points[i][0]
                totals[j][1] += points[i][1]
                #clusters[j] = [totals[j][0]/counts[j], totals[j][1]/counts[j]]
                added = True
                break
        if added == False:
            clusters.append(copy.copy(points[i]))
            totals.append(copy.copy(points[i]))
            counts.append(1)
    return clusters, counts, totals
    
def grid(resolution=65):
    points = []
    for i in range(resolution):
        for j in range(resolution):  
            points.append([left + j * ((right - left)/resolution), bottom + i * ((top - bottom)/resolution)])
    return points
            
def get_index(point, resolution):
    i = math.floor((point[0] - left) / ((right - left)/resolution))
    j = math.floor((point[1] - bottom) / ((top - bottom)/resolution))
    return i + (j * resolution)
    
def get_grid_number(data, index, resolution=65):
    count = []
    for i in range(resolution ** 2):
        count.append(0)
    for i in range(len(index)):
        for j in range(len(data[index[i]]["PATH"])):
            if get_index(data[index[i]]["PATH"][j], resolution) < resolution ** 2 and get_index(data[index[i]]["PATH"][j], resolution) > 0:
                count[get_index(data[index[i]]["PATH"][j], resolution)] += 1
    return count
    
def get_grid_number_points(points, resolution=65):
    count = []
    for i in range(resolution ** 2):
        count.append(0)
    for i in range(len(points)):
        if get_index(points[i], resolution) < resolution ** 2 and get_index(points[i], resolution) > 0:
            count[get_index(points[i], resolution)] += 1
            
    return count
def get_image(image):
    return Image.open(os.path.join(os.getcwd(), image)).convert('RGB')    
    
def color_map(count):
    res = int(len(count) ** (1/2))
    full = max(count)
    l = 1185
    u = 281
    d = 2564
    r = 3261
    
    image = get_image("campus.png")
    #pixel_map = image.load()
    draw = ImageDraw.Draw(image, "RGBA")
    for i in range(res):
        for j in range(res):
            draw.rectangle((l + j * (r - l)/res, (u + i * (d - u)/res), (l + (j + 1) * (r - l)/res, (u + (i + 1) * (d - u)/res))), fill=(255, 0, 0, int((count[j + (res - i - 1) * res]/full)*255)))
    image.save('map_test.png')
    return image
    
def find_triples(data):
    index = []
    for i in range(len(data)):
        if data[i]["RESIDENTIAL"] == "Yes" and data[i][" COMMERCIAL"] == " Yes" and data[i][" TRANSPORTATION"] == " Yes":
            index.append(i)
    return index
    
def save_points_csv(points, name):
    f = open(name + ".csv","w+")
    f.write("LONG,LAT\n")
    for i in range(len(points)):
        f.write(str(points[i][0]) + "," + str(points[i][1]) + "\n")
    f.close()