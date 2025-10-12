import google.generativeai as genai
import os
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def get_user_location() -> str:
    "Gets the users current location and returns a string with the city name"
    return "Cambridge"

model = genai.GenerativeModel('gemini-2.5-flash', tools=[get_user_location])
chat = model.start_chat(enable_automatic_function_calling=True)

prompt = input("Enter prompt or enter 'exit' > ")
while prompt!='exit':
    response = chat.send_message(prompt)
    print(response.text)
    prompt = input("Enter prompt or enter 'exit' > ")