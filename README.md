# cambridge.agentic_ai

Made during my time at cambridge as an intro to agentic ai - ai was used to speed up development process (wrote some code) tasks are shown:


- Hello world. Build a simple command line python app that sendas a hard coded prompt to Gemini and prints the response to screen (as per the lecture).

- Hello world chat. Adapt your hello world app to take prompts from the command line and act as a chatbot. i.e. you type, it responds, you type, it responds, etc.  Make sure you use themodel in caht mode so it builds a history for the chat.

- DIY chat. Imagine that the chat functionality wasn't built in. Adapt your solution for 2 so that you build the history of the chat and supply it to the next prompt. The easy was to do this is to save the full chat so far and provide that as part of the prompt. However, this is inefficient 9and costly because it uses up expensive tokens. A lot of the chat is actually rather redundant, so what you want to do is to summarise the chat so far when you put it in the next prompt.  But LLMs are great at summarising! So try using the LLm to create a summary of the chat so far in the background, ready for it to be fed into the next user prompt.

- Tool use. Recreate the example from lectures that allows the user to ask about the weather in natural language. Experiement with changing the prompt and adding a system prompt. For bonus points, connect it to an actual weather service (use a chatbot to figure out how to pull the data into yout python program).

- Multimodel input. All of the models can take images as input. Write a program that takes in an image on the command line and then presents a chat interface that allows the user to chat about the provided image. (Hint: use a chatbot to help you understand how you might do this). 

- Classification.  Build a program with a UI interface that has a simple window of text that allows a paragraph or so of text to be pasted in and a button. When the button is pressed, you should use gemini to classify the text sentiment (positive, neutral, negative) and change the colour of the text according to that classification (red for negative, blue for neutral, green for positive). Use a chatbot to help you create a UI (one of the easiest libraries for this is pygame). Note: for this one you won't be able to run a GUI inside a Github codespace so you'd need to run it locally. If that isn't possible, make it a command line program that just prints the sentiment.. . 

IMO chat_custom.py is the most interesting.
