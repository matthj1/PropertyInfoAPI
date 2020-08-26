import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE, {
    "search_area": "REGION%5E475",
    "max_bedrooms": 3,
    "min_bedrooms": 1,
    "max_price": 280000,
    "min_price": None,
    "show_bungalow": True,
    "show_detached": True,
    "show_semi-detached": True,
    "show_terraced": True,
    "show_flat": True,
    "show_land": True,
    "must_have_garden": False,
    "must_have_parking": False,
    "dont_show_new-home": False,
    "dont_show_retirement": False,
    "dont_show_shared-ownership": False
})

print(response.json())
print(response)

response2 = requests.get("http://127.0.0.1:5000/pending/0")
print(response2.json())

response3 = requests.get("http://127.0.0.1:5000/completed/0")
print(response3.json())
