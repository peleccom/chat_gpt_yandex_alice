import gpt

from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def main():
    ## Создаем ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    ## Заполняем необходимую информацию
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res,req):
    if req['request']['original_utterance']:
        ## Проверяем, есть ли содержимое
        messages = None
        try:
            reply, messages = gpt.query(req['request']['original_utterance'], messages)
            print(reply)
        except Exception as e:
            print(e)
            reply = 'Не удалось получить ответ'
        res['response']['text'] = reply
        print(res)
    else:
        ## Если это первое сообщение — представляемся
        res['response']['text'] = "Я, умный chatgpt бот. Спроси что-нибудь"

if __name__ == '__main__':
    app.run(host="0.0.0.0")
