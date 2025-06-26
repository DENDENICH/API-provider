FROM python:3.13-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Копирование entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Установка рабочей директории
WORKDIR /app

ENV ALREADY_CONFIGURED=TRUE

CMD ["/entrypoint.sh"]
