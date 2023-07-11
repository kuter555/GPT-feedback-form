import get_requests

conversation = """Classify what a user thought of a show from a conversation with a chatbot:

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


'Hi there! How did you enjoy the theatre show?
I did enjoy hte show
That's great to hear! What did you like about the show the most?
My main thing that I liked was all the acting
Fantastic! Which actor impressed you the most and in what way?
I think that jared was really good becasue he was the funniest
That's great to hear! Could you tell me more about the humor in the show? Did you find it entertaining and appropriate for all ages?
I found it funny for myself, probably not for 20 year olds (they're too cool)
Thanks for sharing that with me! Apart from the acting and humour, were there any other aspects of the show that you appreciated or thought could be improved upon?
The seating could have been better
Thanks for the feedback! Regarding the seating, what specifically could have been improved upon to make it a better experience for you?
comfier seats
Thanks! That's certainly something that the theatre management could take note of. Thank you again for sharing your thoughts with me. Enjoy the rest of your day! DONE.':

"""

payload = {
        "prompt": conversation,
        "max_tokens": 45
    }

response = get_requests.get_response(payload, "text-davinci-003")['choices'][0]['text']

print(response)
with open("data.txt", "w") as f:
    f.write(response)