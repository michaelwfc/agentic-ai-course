from google import genai
from google.genai.types import HttpOptions



def run_genai_client():
  client = genai.Client(http_options=HttpOptions(api_version="v1"))
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents="what specific google model do you use" #"How does AI work?",
  )
  print(response.text)
  # Example response:
  # Okay, let's break down how AI works. It's a broad field, so I'll focus on the ...
  #
  # Here's a simplified overview:
  # ...
  

if __name__ == "__main__":
  run_genai_client()
  