FROM python:3

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

RUN pip install matplotlib numpy tk customtkinter

COPY . . 

EXPOSE 5015

CMD ["python", "./custom.py"]