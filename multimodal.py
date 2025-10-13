"""This takes in an image when run in terminal and uses it as context for every message sent
e.g. python3 multimodal.py <path/to/image>"""
import os
import sys
import google.generativeai as genai
import PIL.Image

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')
chat = model.start_chat()

try:
    # The first command-line argument is the script name, so we start from index 1
    image_path = sys.argv[1]
except IndexError:
    print("Error: Please provide an image file path.")
    print("Usage: python your_script_name.py \"Your prompt here\" path/to/image.jpg")
    sys.exit(1)

img = PIL.Image.open(image_path)

prompt = input("Enter prompt or enter 'exit' > ")
while prompt!='exit':
    response = chat.send_message([prompt, img])
    print(response.text)
    prompt = input("Enter prompt or enter 'exit' > ")
print("Goodbye!")
