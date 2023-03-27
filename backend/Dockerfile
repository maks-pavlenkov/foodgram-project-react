FROM python:3.7-slim
WORKDIR /app
COPY backend/requirements.txt .
# RUN apt-get update \
#     && apt-get -y install libpq-dev gcc \
#     && pip install psycopg2
# RUN pip3 install psycopg2
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
# COPY ../data/ .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]