FROM python:3.12.6
WORKDIR /docker/avtoshina_38_bot/src
COPY requirements.txt /docker/avtoshina_38_bot/src
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /docker/avtoshina_38_bot/src

CMD [ "python", "start_bot.py"]