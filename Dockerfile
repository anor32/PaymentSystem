FROM python:3.12-slim


WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .




EXPOSE 8000

CMD ["/code/entrypoint.sh"]