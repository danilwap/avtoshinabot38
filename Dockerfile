FROM python:3.12.6
WORKDIR /src/app/
COPY . /src/app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt


CMD ["python start_bot.py"]