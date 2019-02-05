def sorted_distance(origins,destination):
    import requests
    import json
    import os

    SECRET_BING_KEY_1 = os.environ.get("Distance_key")
    url="https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix"
    locations="?origins="+origins+"&destinations="+destination
    driving_mode="&travelMode=driving"

    key = "&key="+str(SECRET_BING_KEY_1)
    u=url+locations+driving_mode+key
    search_results = requests.get(u)
    Results=json.loads(search_results.text)
    #print(Results)
    resources=Results["resourceSets"][0]["resources"][0]['results'][0]
    return resources["travelDistance"],resources["travelDuration"]


