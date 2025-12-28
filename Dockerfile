FROM python:3.12


WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN echo 'starting project'



