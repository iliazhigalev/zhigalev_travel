# Используем официальный образ Python
FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Даём права на выполнение entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Указываем скрипт запуска
ENTRYPOINT ["/app/entrypoint.sh"]
