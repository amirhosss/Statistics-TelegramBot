FROM python:3.10.6-slim
WORKDIR /telegrambot
COPY . /telegrambot
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
# CMD ["python3", "main.py"]