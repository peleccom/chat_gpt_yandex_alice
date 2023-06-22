import asyncio
import traceback
from typing import Union
from fastapi import FastAPI, Request

import datetime
from dotenv import load_dotenv
from session import UserSession
load_dotenv()
import gpt

app = FastAPI()
answers = dict()

CUT_WORD = ['Алиса', 'алиса']

users_state = dict()

@app.post("/post")
async def post(request: Request):
    request = await request.json()
    response = {
        'session': request['session'],
        'version': request['version'],
        'response': {
            'end_session': False
        }
    }
    ## Заполняем необходимую информацию
    await handle_dialog(response, request)
    print(response)
    return response

async def handle_dialog(res,req):
    print('start handle:', datetime.datetime.now(tz=None))
    print(req)
    session_id = req['session'].get('session_id')
    print('userid', session_id)

    session_state = UserSession.get_state(session_id)
    request_message = req['request']['original_utterance']

    ## Проверяем, есть ли содержимое
    if request_message:
        for word in CUT_WORD:
            if request_message.startswith(word):
                request_message = request_message[len(word):]
        request_message = request_message.strip()


        if 'message' not in session_state:
            await Dialog.first_message(request_message, session_state, res)
        else:
            await Dialog.second_message(request_message, session_state, res)
    else:
        await Dialog.init_chat(request_message, session_state, res)
        ## Если это первое сообщение — представляемся
    print('end handle:', datetime.datetime.now(tz=None))

class Dialog:
    @staticmethod
    async def init_chat(request_message , state, res):
        reply = 'Я умный chat бот. Спроси что-нибудь'
        res['response']['text'] = reply

    @staticmethod
    async def first_message(request_message , state, res):
        task = asyncio.create_task(ask(request_message, state['messages']))
        await asyncio.sleep(1)
        state['messages'].append(request_message)
        if task.done():
            reply = task.result()
            res['response']['text'] = reply
            del answers[request_message]
        else:
            print('no response')
            reply = 'Не успел получить ответ. Спросите позже'
            res['response']['text'] = reply
            res['response']['tts'] = reply + '<speaker audio="alice-sounds-things-door-2.opus">'
            state['message'] = request_message

    @staticmethod
    async def second_message(request_message , state, res):
        old_request = state['message']
        if old_request not in answers:
            reply = 'Ответ пока не готов, спросите позже'
            res['response']['text'] = reply
            res['response']['tts'] = reply + '<speaker audio="alice-sounds-things-door-2.opus">'
        else:
            answer = answers[old_request]
            del answers[old_request]
            del state['message']
            reply = f'Отвечаю на предыдущий вопрос "{old_request}"\n {answer}'
            res['response']['text'] = reply


async def ask(request, messages):
    try:
        reply = await gpt.aquery(request, messages)
    except Exception as e:
        traceback.print_exc()
        reply = 'Не удалось получить ответ'
    answers[request] = reply
    print('get response from gpt:', datetime.datetime.now(tz=None))
    return reply


