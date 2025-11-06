FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git build-essential

COPY driver.json driver.json
COPY requirements.txt requirements.txt
COPY ./uc_intg_xbox_live ./uc_intg_xbox_live

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

ADD . .

ENV UC_DISABLE_MDNS_PUBLISH="false"
ENV UC_MDNS_LOCAL_HOSTNAME=""
ENV UC_INTEGRATION_INTERFACE="0.0.0.0"
ENV UC_INTEGRATION_HTTP_PORT="9099"
ENV UC_CONFIG_HOME="/config"

CMD ["python3", "-u", "./uc_intg_xbox_live/driver.py"]
