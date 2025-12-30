FROM python:3.12-slim


WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /code/entrypoint.sh
RUN python manage.py collectstatic --noinput

EXPOSE  10000

CMD ["/code/entrypoint.sh"]