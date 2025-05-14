FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir waitress -r requirements.txt

# Для удобства разработки не будем включать код приложения в контейнер
# После завершения разработки можно раскомментить строку ниже.
# Но тогда необходимо будет создать volumes в docker-compose:
#  - ./app/media: /app/app/media   # Для сохранения загруженных картинок
#  - ./app/data: /app/app/data     # Для сохранения БД

#COPY app .

EXPOSE 5000
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]