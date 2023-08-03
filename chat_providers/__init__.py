import os
from dotenv import load_dotenv


load_dotenv()
chat_provider = os.environ.get('CHAT_PROVIDER')

def dummy():
    from .dummy import aquery as _aquery
    return _aquery

def open_ai():
    from .openai import aquery as _aquery
    return _aquery

def gpt4free_you():
    from .gpt4free_you import aquery as _aquery
    return _aquery

PROVIDERS_MAP= {
    'DUMMY': dummy,
    'OPEN_AI':  open_ai,
    'GPT4FREE_YOU': gpt4free_you,
}

if chat_provider in PROVIDERS_MAP:
    aquery = PROVIDERS_MAP[chat_provider]()
else:
    raise ValueError(f'Unknown chat provider {chat_provider}. Available choices are {list(PROVIDERS_MAP.keys())}')
