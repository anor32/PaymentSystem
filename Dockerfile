FROM python:3.12


WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN echo 'starting project'
RUN python manage.py makemigrations && python manage.py migrate && python manage.py loaddata fixtures/payments.json && python manage.py loaddata fixtures/users.json && python  manage.py runserver