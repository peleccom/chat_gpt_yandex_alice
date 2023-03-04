FROM python:3.9-slim
WORKDIR /app

# RUN apk update && apk add gcc musl-dev
RUN printf "[global] \n extra-index-url=https://www.piwheels.org/simple" > /etc/pip.conf

COPY requirements.txt requirements.txt
RUN MAKEFLAGS=-j$(nproc) pip3 install -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1
CMD [ "uvicorn", "main:app", "--host",  "0.0.0.0", "--port",  "5000" ]
