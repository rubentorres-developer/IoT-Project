FROM python:3.11.7

WORKDIR /kernel

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./kernel.py .

CMD ["python", "kernel.py"]
