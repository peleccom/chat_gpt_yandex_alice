import os

import openai


OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

def query(message, prev_messages=None):
    if not prev_messages:
        messages = []
    else:
        messages = prev_messages


    messages.append({"role": "user", "content": message})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
    reply = chat.choices[0].message.content
    reply = reply.strip()
    return reply, messages
