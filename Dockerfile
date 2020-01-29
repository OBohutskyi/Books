FROM python:3.8
RUN mkdir /workdir
WORKDIR /workdir
COPY requirements.txt /workdir/
COPY db.sqlite3 /workdir/
COPY manage.py /workdir/
RUN pip install -r requirements.txt
python manage.py runserver