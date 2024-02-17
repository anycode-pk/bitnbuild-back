import requests

import json

response = requests.get('http://127.0.0.1:5000/modules/12', json={"title": "Test3", "image_url": "test.com", "description": "Test"})
print(response.json())