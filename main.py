import asyncio
import traceback
from fastapi import FastAPI, Request
import gpt
import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
answers = dict()

CUT_WORD = ['Алиса', 'алиса']


@app.post("/post")
async def post(request: Request):
    request = await request.json()
    response = {
        'session': request['session'],
        'version': request['version'],
        'session_state': request.get('state', {}).get('session', {}),
        'response': {
            'end_session': False
        }
    }
    # Заполняем необходимую информацию
    await handle_dialog(response, request)
    print(response)
    return response


async def handle_dialog(res, req):
    print('start handle:', datetime.datetime.now(tz=None))
    print(req)
    if req['request']['original_utterance']:
        session_state = res.get('session_state', {})
        # Проверяем, есть ли содержимое
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
        # Если это первое сообщение — представляемся
    res['response']['text'] = reply
    print('end handle:', datetime.datetime.now(tz=None))


async def ask(request, messages):
    try:
        reply = await gpt.aquery(request, messages)
    except Exception as e:
        print(f"Smth error: {e}")
        traceback.print_exc()
        reply = 'Не удалось получить ответ'
    answers[request] = reply
    print('get response from gpt:', datetime.datetime.now(tz=None))
    return reply
