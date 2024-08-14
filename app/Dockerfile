FROM python:3.12.3-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "insert_data_to_database.py"]


