import requests
import time

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE, {
    "search_area": "REGION%5E475",
    "max_bedrooms": 3,
    "min_bedrooms": 2,
    "max_price": 260000,
    "min_price": None,
    "show_house_type": ["flat", "detached", "semi-detached", "terraced"],
    "must_have": [],
    "dont_show": []
})

print(response.json())
print(response)

if response:
    uri_progress = response.json()["URI_Pending"]
    pending_request = requests.get(uri_progress)
    print(pending_request.json() + " is pending request")
    while pending_request.json() == "Search in progress":
        print("Waiting for request to finish")
        time.sleep(2.0)
        pending_request = requests.get(uri_progress)
    uri_complete = pending_request.json()["URI_Complete"]
    data = requests.get(uri_complete)
    print(data.json())
