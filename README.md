# GPT-feedback-form
Creating a ChatGPT powered feedback form for the Edge theatre, which is designed to be sent to people who went to see shows and to get more tailored responses from them.

Created during summer 2023 as part of a research internship at the University of Bath, thsi program will not work without an API key. 

## How it works

This project is a test of what LLMs can do. One of the main problems with integrating LLMs into user-facing roles is that people will always try and "Jailbreak" the chatbot. To get around this, there are multiple steps in this project that aim to circumvent this - which I describe as *three prong prompting*. Firstly - safeguarding. This project doesn't want to allow people to talk to it and confess welfare-related issues, only for them to be ignored by the chatbot. This is the first test, which makes sure that their prompt isn't safeguarding related. 

Then - we have the security prompt, which checks if their message is trying to jailbreak the system. This took a while to make work, as there are always ways to get around "forced prompting". However, to get around this I used similar methods from SQL-injection protection, which avoids the potentially dangrerous prompts from entering the flow of the message.

Finally, we actually send the prompt to the "proper" chatbot, which generates a response.

## OpenAI Api

This project was developed towards the beginning of the use of the OpenAI API, which means that I had very little to base the way that API calls should be made. 
