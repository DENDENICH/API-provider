FROM python:3.13-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Копируем entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Устанавливаем рабочую директорию
WORKDIR /app

ENV ALREADY_CONFIGURED=TRUE

CMD ["/entrypoint.sh"]
