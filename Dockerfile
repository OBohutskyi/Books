FROM python:3.8
COPY . /workdir
WORKDIR /workdir
RUN pip install -r requirements.txt