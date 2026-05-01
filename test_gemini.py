from dotenv import load_dotenv
from google import genai
import os
 
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key: 
    print("Fehler funktioniert nicht :( ")
    exit()

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Antworte nur mit: Gemini funktioniert."
)

print(response.text)