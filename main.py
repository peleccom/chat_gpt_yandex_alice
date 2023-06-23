import asyncio
import traceback
from typing import Union
from chat_providers import aquery
from fastapi import FastAPI, Request

import datetime
from session import UserSession
from utils import split_text_to_chunks

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
    if res['response']['text'] and len(res['response']['text']) > 1024:
        res['response']['text'] = res['response']['text'][:1024]
        print(len(res['response']['text']))
    if 'tts' in res['response'] and len(res['response']['tts']) > 1024:
        res['response']['tts'][:1024]
    print('end handle:', datetime.datetime.now(tz=None))

class Dialog:
    @staticmethod
    async def init_chat(request_message , state, res):
        reply = 'Я умный chat бот. Спроси что-нибудь'
        res['response']['text'] = reply

    @staticmethod
    async def first_message(request_message , state, res):
        task = asyncio.create_task(process_answer(request_message, state['messages']))
        await asyncio.sleep(1)
        state['messages'].append(request_message)
        if task.done():
            ready, chunk, last = consume_answer(request_message)
            reply = chunk
            res['response']['text'] = reply
            state['message'] = request_message

            if last:
                del state['message']
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
            del state['message']
            reply = 'Ответ пока не готов, спросите позже'
            res['response']['text'] = reply
            res['response']['tts'] = reply + '<speaker audio="alice-sounds-things-door-2.opus">'
            return
        else:
            ready, chunk, last = consume_answer(old_request)
            if not ready:
                reply = ''
                res['response']['text'] = reply
                res['response']['tts'] = reply + '<speaker audio="alice-sounds-things-door-2.opus">'
                return
            else:
                reply = chunk
                res['response']['text'] = reply

                if last:
                    del state['message']


async def ask(request, messages):
    try:
        reply = await aquery(request, messages)
    except Exception as e:
        traceback.print_exc()
        reply = 'Не удалось получить ответ'
    answers[request] = reply
    print('get response from gpt:', datetime.datetime.now(tz=None))
    return reply


async def process_answer(request, messages):
    answer_info = {
        'ready': False,
        'cur_chunk': 0,
        'chunks': [],
    }
    answers[request] = answer_info

    MAX_SIZE = 1024
    answer_reply = await ask(request, messages)

    chunks = split_text_to_chunks(
        answer_reply,
        MAX_SIZE,
        answer_prefix = f'Продолжаю ответ на предыдущий вопрос "{request}"\n',
        answer_postfix = 'Продолжить?',
        first_answer_prefix=f'Отвечаю на предыдущий вопрос "{request}"\n',
    )

    answer_info = {
        'ready': True,
        'cur_chunk': 0,
        'chunks': chunks,
    }
    answers[request] = answer_info
    return answer_info

def consume_answer(request):
    answer_info = answers[request]
    if answer_info['ready']:
        chunks = answer_info['chunks']
        chunk = chunks[answer_info['cur_chunk']]
        last = False
        if answer_info['cur_chunk'] == len(chunks) - 1:
            # consumed all
            del answers[request]
            last = True
        else:
            answer_info['cur_chunk'] += 1
        return True, chunk, last
    return False, None, False
