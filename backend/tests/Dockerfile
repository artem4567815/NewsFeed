FROM python:3.12

WORKDIR /tests

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest"]
