FROM python:3.12.0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]
