FROM python:3.10.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "/bin/bash", "./run.sh" ]

