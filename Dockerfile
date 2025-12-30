FROM python:3.12-slim


WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .


RUN echo '#!/bin/bash\n\
python manage.py makemigrations\n\
python manage.py migrate\n\
python manage.py loaddata fixtures/payments.json\n\
python manage.py loaddata fixtures/users.json\n\
python manage.py runserver 0.0.0.0:8000' > /code/entrypoint.sh && chmod +x /code/entrypoint.sh

EXPOSE 8000

CMD ["/code/entrypoint.sh"]