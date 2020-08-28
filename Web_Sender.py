import requests
import time

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE, {
    "search_area": "REGION%5E475",
    "max_bedrooms": 3,
    "min_bedrooms": 1,
    "max_price": 280000,
    "min_price": None,
    "show_house_type": ["flat", "detached", "semi-detached", "terraced"],
    "must_have": [],
    "dont_show": []
})

print(response.json())
print(response)

if response:
    uri_progress = response.json()["URI"]
    pending_request = requests.get(uri_progress)
    print(pending_request.json() + " is pending request")
    while pending_request.json() == "Search in progress":
        print("Waiting for request to finish")
        time.sleep(5.0)
        pending_request = requests.get(uri_progress)
    data = requests.get(uri_progress)
    print(data.json())
