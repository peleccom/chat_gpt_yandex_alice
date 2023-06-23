FROM python:3.9-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ARG PYTHONUNBUFFERED=1
RUN printf "[global] \n extra-index-url=https://www.piwheels.org/simple" > /etc/pip.conf

COPY requirements.txt requirements.txt
COPY postinstall.sh .
RUN MAKEFLAGS=-j$(nproc) pip3 install --no-cache-dir -r requirements.txt && sh postinstall.sh

COPY . .

CMD [ "uvicorn", "main:app", "--host",  "0.0.0.0", "--port",  "5000" ]
