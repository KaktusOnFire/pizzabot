FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1

COPY ./req.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/

ENV API_TOKEN="SUPER SECRET KEY"

CMD [ "python", "main.py" ]