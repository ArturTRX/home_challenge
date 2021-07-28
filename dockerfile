FROM python:3.8.0

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

COPY req.txt req.txt

RUN pip install -r req.txt

COPY . .

CMD ["python", "main.py"]
