FROM python:3.8

WORKDIR /codacy

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /codacy/app

EXPOSE 8080

CMD ["python3", "api.py"]