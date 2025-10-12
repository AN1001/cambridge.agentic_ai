"Emulates a chat with AI, stores and highly compresses context"
import google.generativeai as genai
import os
import datetime
import json
import random

cache:dict[str,str] = {
    "current_time":datetime.datetime.now().strftime('%m/%d/%Y'),
    "name":"unknown"
}
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    system_instruction="""
    You are answering the users questions (indicated by <<answer>>), you
    will be given context (as a python dict) beforehand of previous important information
    you may be asked to summarise users response and add it to context,
    context may contain numbers in keys to prevent duplicate keys; ignore this.
    If asked to summarise (indicated by <<summarise>>) return a python dict key
    and the summary seperated by a colon (:) and nothing else e.g.

    Input:Hi my name is John doe
    Output:Hello i'm here to help!
    your summary: name:John doe

    Input: How do you make a falafel
    output: First grind and mix spinach with chickpeas followed by hummus
    and then fry
    your summary: previous_response:falafel instructions including grind,mix spinach with chickpeas and hummus then fry

    DO NOT OUTPUT SUMMARY WHEN <<answer>> FLAG PRESENT.
    """

)
def get_context(cache:dict[str,str]) -> str:
    """
    Takes context in dictionary
    form and returns it as a string
    for LLM use in prompt
    """
    return json.dumps(cache)

def add_context(input:str, response:str, cache:dict[str,str]) -> None:
    """
    Takes previous response and input and uses an LLM
    to summarise and add important info to the cache
    """
    prompt = f'<<summarise>>Input: {input}\nOutput:{response}'
    llm_response = model.generate_content(prompt)
    data = llm_response.text.split(":")
    
    cache[data[0]+str(random.randint(1000,9999))]=data[1]

def clean_text(text:str) -> str:
    """
    Cleans text by removing flags <<summarise>> and <<answer>>
    This to prevent LLM being confused at what action to take
    and to prevent code injection attack
    """
    return text.replace("<<answer>>", "").replace("<<summarise>>", "")

prompt = input("Enter prompt or enter 'exit' > ")
while prompt!='exit':
    response = model.generate_content(get_context(cache)+"<<answer>>"+clean_text(prompt))
    print(response.text)
    add_context(prompt,clean_text(response.text),cache)
    prompt = input("Enter prompt or enter 'exit' > ")
    if prompt=="exit":
        response = model.generate_content(
            get_context(cache)
            +"<<answer>>User wants to leave, send a nice goodbye message"
        )
        print(response.text)
