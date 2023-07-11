import openai
import os
deployment_names = ['gpt-3.5-turbo', 'text-davinci-003'] # this is the model you are requesting
# send a payload and get a response from azure openai
def gpt_response(messages, model=deployment_names[0], max_tokens=30, temperature=1):

    response = openai.ChatCompletion.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )

    # return the response from the model
    return response


# sends and receives a payload using the davinci model
def davinci_response(messages, model=deployment_names[1], max_tokens=30, temperature=0):

    response = openai.Completion.create(
        prompt=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )

    # return the payload from the model
    return response
