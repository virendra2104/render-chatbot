import requests

URL = "http://localhost:9000/mcp"

payload = {
    "tool": "add_registration",
    "args": {
        "name": "Virendra Kumar",
        "email": "virendra@gmail.com",
        "phone": "9876543210",
        "course": "Data Engineering"
    }
}

response = requests.post(URL, json=payload)

print("Status:", response.status_code)
print("Response:", response.json())
