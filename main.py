import asyncio
import traceback
from typing import Union
from fastapi import FastAPI, Request

import datetime
from dotenv import load_dotenv
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
    if session_id and not session_id in users_state:
        users_state[session_id] = {
            'messages': [],
        }

    if session_id:
        session_state = users_state[session_id]
    else:
        session_state = {}

    if req['request']['original_utterance']:
        ## Проверяем, есть ли содержимое
        messages = session_state.get('messages', [])
        request = req['request']['original_utterance']
        for word in CUT_WORD:
            if request.startswith(word):
                request = request[len(word):]
        request = request.strip()


        if 'message' not in session_state:
            task = asyncio.create_task(ask(request, messages))
            await asyncio.sleep(1)
            messages.append(request)
            session_state['messages'] = messages
            if task.done():
                reply = task.result()
                del answers[request]
            else:
                print('no response')
                reply = 'Не успел получить ответ. Спросите позже'
                res['response']['tts'] = reply + '<speaker audio="alice-sounds-things-door-2.opus">'
                session_state['message'] = request
        else:
            old_request = session_state['message']
            if old_request not in answers:
                reply = 'Ответ пока не готов, спросите позже'
                res['response']['tts'] = reply + '<speaker audio="alice-sounds-things-door-2.opus">'
            else:
                answer = answers[old_request]
                del answers[old_request]
                del session_state['message']
                reply = f'Отвечаю на предыдущий вопрос "{old_request}"\n {answer}'
    else:
        reply = 'Я умный chat бот. Спроси что-нибудь'
        ## Если это первое сообщение — представляемся
    res['response']['text'] = reply
    print('end handle:', datetime.datetime.now(tz=None))

async def ask(request, messages):
    try:
        reply = await gpt.aquery(request, messages)
    except Exception as e:
        traceback.print_exc()
        reply = 'Не удалось получить ответ'
    answers[request] = reply
    print('get response from gpt:', datetime.datetime.now(tz=None))
    return reply
