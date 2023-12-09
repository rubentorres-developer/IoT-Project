FROM python:3.11.7

WORKDIR /processor

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]
