FROM python:3.12.0

WORKDIR /app

COPY .env .env

COPY requirements.txt .

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

COPY ./app /app

EXPOSE 5000

CMD ["python3", "main.py"]
