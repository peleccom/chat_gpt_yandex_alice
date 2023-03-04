FROM python:3.8-alpine
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ARG OPENAI_API_KEY # you could give this a default value as well
ENV OPENAI_API_KEY=$OPENAI_API_KEY

CMD [ "python3", "bot.py"]
