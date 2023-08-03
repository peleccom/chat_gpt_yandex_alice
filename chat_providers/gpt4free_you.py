import os
import asyncio
from gpt4free import you

async def aquery(message, prev_messages=None):
    chat = []
    for req, res in prev_messages:
        chat.append({"question": req, "answer": res})

    # response = await you.Completion.create(
    #     prompt=message,
    #     chat=chat)

    loop = asyncio.get_event_loop()
    print(chat      )

    response = await loop.run_in_executor(None, lambda xй: you.Completion.create(
        prompt=message,
        chat=chat), 50)

    text = response.text
    text = text.encode().decode("unicode_escape")
    return text
