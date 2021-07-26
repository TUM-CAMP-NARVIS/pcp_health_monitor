FROM python:3.9-buster

RUN apt-get update && apt-get install -y --no-install-recommends git pkgconf libxml2 libxslt1.1 cmake libxml2-dev libxslt1-dev build-essential

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install git+https://github.com/capnproto/pycapnp@v1.0.0#egg=pycapnp

COPY . .

EXPOSE 8888
ENV PYTHONPATH=/usr/src/app

CMD [ "python", "./health_monitor", "--config", "./resources/config/mobile.yml"]
