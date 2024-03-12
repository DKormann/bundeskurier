#%% 
import requests
import dotenv


MISTRAL_API_KEY = dotenv.get_key("./.env","MISTRAL_API_KEY")


def fetch_answer(prompt:str):
  return chat_complete([{"role": "system", "content": prompt}])

def chat_complete(messages: list):
  url = "https://api.mistral.ai/v1/chat/completions"
  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {MISTRAL_API_KEY}"
  }
  data = {
    "model": "mistral-large-latest",
    "messages": messages
  }
  response = requests.post(url, headers=headers, json=data)
  data = response.json()
  print(data)
  resp = data['choices'][0]['message']['content']
  return resp

if __name__ == "__main__": print(fetch_answer("What is the meaning of life?"))