from flask import Flask, request ,redirect
from test3Copy import sorted_distance
import requests
import json
import os

SECRET_BING_KEY = os.environ.get("ORIGIN_key")


app = Flask(__name__)

@app.route('/query-example')
def query_example():
    categ=request.args["categ"]
    lat=request.args["lat"]
    longit=request.args["longit"]


    url = "https://dev.virtualearth.net/REST/v1/LocalSearch/?query="+categ+"&userLocation="+str(lat)+","+str(longit)+"&key="+str(SECRET_BING_KEY)

    re = requests.get(url)
    returning = json.loads(re.text)

    Dict = {}
    temp_dict=[1000000,1000000]
    origin=lat+","+longit
    origin=str(origin)
    for i in range(len(returning['resourceSets'][0]['resources'])-1):
        Result_name = returning['resourceSets'][0]['resources'][i]['name']
        Result_coordinates = returning['resourceSets'][0]['resources'][i]['point']['coordinates']
        Result_coordinates=str(Result_coordinates[0])+","+str(Result_coordinates[1])
        Result_Address=returning['resourceSets'][0]['resources'][i]["Address"]['formattedAddress']
        PhoneNumber=returning['resourceSets'][0]['resources'][i]['PhoneNumber']

        Dict[str(i)] = [Result_name,Result_coordinates,Result_Address,PhoneNumber]

        present_dist,present_time=sorted_distance(str(origin),str(Result_coordinates))
        if (present_time+((i+1)*10))<=temp_dict[1]:
            temp_dict[0]=present_dist
            temp_dict[1]=present_time
            temp_index=i
        else:
            continue

    Dict[str(temp_index)].append(str(present_dist)+" Kms")
    Dict[str(temp_index)].append(str(present_time) + " Minutes")
    if ("map" in request.args):
        if request.args["map"]=="1":
            return redirect("https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes?wp.0="+str(origin)+";64;1&wp.1="+str(Result_coordinates)+";66;2&key="+str(SECRET_BING_KEY), code=302)
        else:
            return json.dumps(Dict[str(temp_index)])
    else:
        return json.dumps(Dict[str(temp_index)])


if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000