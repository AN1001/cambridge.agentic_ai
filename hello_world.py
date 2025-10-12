import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-2.5-flash-lite')

prompt = 'Who invented the python language?'
response = model.generate_content(prompt)

print(response.text)