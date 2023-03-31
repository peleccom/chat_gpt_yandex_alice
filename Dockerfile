FROM python:3.9-slim
WORKDIR /app

COPY . .

RUN printf "[global] \n extra-index-url=https://www.piwheels.org/simple" > /etc/pip.conf && \
    MAKEFLAGS=-j$(nproc) pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1
CMD [ "uvicorn", "main:app", "--host",  "0.0.0.0", "--port",  "5000" ]
