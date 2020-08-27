import requests

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

response2 = requests.get("http://127.0.0.1:5000/pending/0")
print(response2.json())

response3 = requests.get("http://127.0.0.1:5000/completed/0")
print(response3.json())
