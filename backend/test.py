from dotenv import load_dotenv
import requests
import openai
import os
import json
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Add your OpenAI API key here
client = openai.OpenAI()
url = "http://127.0.0.1:8000/askchat"
url2 = "http://127.0.0.1:8000/ok"

data = {"text": "i want to cancel order number five"}

resp = requests.post(url, json=data)
#resp = requests.get(url2)
print(resp.text)

