import os
from dotenv import load_dotenv
load_dotenv()
CHAT_PROVIDER = os.environ.get('CHAT_PROVIDER')

if CHAT_PROVIDER == 'DUMMY':
    from .dummy import aquery as _aquery
    aquery = _aquery
elif CHAT_PROVIDER == 'OPEN_AI':
    from .openai import aquery as _aquery
    aquery = _aquery
else:
    raise ValueError(f'Unknown chat provider {CHAT_PROVIDER}')
