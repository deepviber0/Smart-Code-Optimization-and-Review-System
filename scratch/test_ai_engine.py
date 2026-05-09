import requests
try:
    response = requests.post('http://127.0.0.1:5001/analyze', json={'code': 'print(1)', 'language': 'python'})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
