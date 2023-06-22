import os

import openai

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
async def aquery(message, prev_messages=None):
    messages = []
    if not prev_messages:
        all_messages = []
    else:
        all_messages = prev_messages.copy()
    all_messages.append(message)
    for m in all_messages:
        messages.append({"role": "user", "content": m})

    chat = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages = messages)
    reply = chat.choices[0].message.content
    reply = reply.strip()
    return reply
