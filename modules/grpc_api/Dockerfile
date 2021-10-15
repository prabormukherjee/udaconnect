FROM python:3.7-slim-buster

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "main.py"]