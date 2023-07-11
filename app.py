from get_requests import gpt_response, davinci_response
from security_check import safe_message
from flask import session, Flask, redirect, render_template, request, url_for
from re import search
from itertools import chain

app = Flask(__name__)

# prompt for starting the interaction
partOne_prompt = '''You are a feedback form for a theatre show.
You are chatbot 1. Your goal is to get the user to share some information about what they liked about the show.
After no more than 3 questions, write COMPLETE at the end of your message.
Ask only one question at a time and make messages less than 20 words long.
Say hi to the user and ask a general question to begin.'''

# prompt for deep diving into the art side of it
partTwo_prompt = '''You are a feedback form for a theatre show.
You are chatbot 2. Your goal is to understand how the show made the user feel emotionally,
what feelings it evoked, how they perceived it as an art piece, and if it reminded them of any other 
works of art.
The conversation so far has been: {}
Finish the conversation in 5 messages or less. Write DONE at the end of your final message.
Ask only one question at a time and make messages less than 20 words long.
Say hi to the user and ask a general question to begin.
'''

# prompt for classifying the conversation into categories
analysis_prompt = """Classify in 4 categories what a user thought of a show from a conversation with a chatbot:

'
Hi! Did you enjoy the show?
Yes i did enjoy the show
What was it that you enjoyed about the show?
I really liked the acting, it was very good
What was it about the acting that you liked the most?
They were really funny. I laughed a lot!
What actor did you think was the funniest?
John was a right laugh :)
Thank you for answering our questionnaire. Your thoughts have helped out the show a lot! DONE.
':

ENJOYABILITY: 4/5
ACTING: 4/5
HUMOR: 4/5
OVERALL SCORE: 5/5
"""

partOne_message = {"role":"system", "content": partOne_prompt}

partOne_messages = [partOne_message]
partTwo_messages = []

@app.route("/", methods=("GET", "POST"))
def index():
    global partOne_messages, partTwo_messages
    #if the form is completed
    if request.method == "POST":
        # obtain the prompt using forms in flask
        prompt = request.form["get_prompt"]
        if(len(partTwo_messages) == 0):
            #update the messages
            partOne_messages.append({"role": "user", "content": prompt})
            partOne_messages.append(gpt_response(partOne_messages, 'gpt-4', 30, 0.8)['choices'][0]['message'])
        else:
            # update the messages
            partTwo_messages.append({"role": "user", "content": prompt})
            partTwo_messages.append(gpt_response(partTwo_messages, 'gpt-4', 30, 0.8)['choices'][0]['message'])
        # store the text variables for the session, so that on refresh it clears
        try:
            session["result"] = [[response['role'], response['content']] for response in chain(partOne_messages, partTwo_messages)]
            session["chats"] = len(session["result"])
        except:
            session["result"] = ["", "There was an error processing your request. Please try again later"]
        # link the url to index so when the refresh, it works
        return redirect(url_for("index"))

    # if a conversation is flowing
    if "result" in session:
        print(partOne_messages[-1]['content'])
        # if the first section has been completed
        if search("COMPLETE.?$", partOne_messages[-1]['content']):
            partOne_messages[-1]['content'] = partOne_messages[-1]['content'][:-9]
            partTwo_messages = [{"role": "system", "content": partTwo_prompt.format(strlist(session["result"]))}]
            partTwo_messages.append(gpt_response(partTwo_messages, 'gpt-4', 30, 0.8)['choices'][0]['message'])
            # store the text variables for the session, so that on refresh it clears
            try:
                print(partTwo_messages[1]["content"])
                session["result"] = session["result"].append(partTwo_messages[1]['role'], partTwo_messages[1]['content'])
                session["chats"] = session["chats"] + 1
            except:
                session["result"] = ["", "There was an error processing your request. Please try again later"]

        if len(partTwo_messages) > 0:
            if search("DONE.?$", partTwo_messages[-1]['content']):
                save_data(analyse_conversation(chain(partOne_messages, partTwo_messages)))


        # get the variables from the session
        result = session.pop("result", '')
        chats = session.pop("chats", 2)

        print(result)
        return redirect(url_for("index"))

    # if this is the first time that we are loading this, or the user refreshes the page
    else:
        partOne_messages = [partOne_message]
        response = gpt_response(partOne_messages, 'gpt-4')['choices'][0]['message']
        # add the previous message to the chat history
        partOne_messages.append(response)
        # extract the text response
        session["result"] = [response['role'], response['content']]
        result = session.pop("result")
        chats = 2

    return render_template("index.html", result=result, chats=chats)

# analyses the conversation
def analyse_conversation(messages):
    conversation = ""
    for message in messages:
        conversation = conversation + message + "\n"
    prompt = analysis_prompt + "\n\n" + "'" + conversation + "'" + ":\n"
    return davinci_response(prompt, "text-davinci-003", 45)['choices'][0]['text']

# turns a list into a string whilst ignoring the first message
def strlist(messages):
    conversation = ""
    for message in messages[1:]:
        conversation = conversation + message[1] + '\n'
    return conversation

# saves the conversation :)
def save_data(data):
    with open("data.txt", "w") as f:
        f.write(data)

if __name__ == '__main__':
    app.run()