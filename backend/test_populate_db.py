import requests

url = "http://127.0.0.1:8000/populate_db/"
data = {"file_path": "pop_db.py"}

response = requests.post(url, data=data)
print(response.json())
