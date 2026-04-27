import requests

payload = {
  "message": "I met Dr. Steve on wednesday April 22. He was in a good mood and asked me about all our new offerings. I showed him our brochure. He ordered 18 new x-ray machines. interaction type was Meeting",
  "current_draft": {}
}
response = requests.post("http://127.0.0.1:8000/api/chat/", json=payload)
print(response.json())
