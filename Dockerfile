FROM python:3.10-alpine as builder

WORKDIR /usr/src/flask_app

ENV PATH /usr/local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && apk add build-base

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /usr/src/flask_app/requirements.txt

RUN python -m pip install -r requirements.txt --prefix=/install



FROM python:3.10-alpine

RUN apk add libpq

COPY --from=builder /install /usr/local/

WORKDIR /usr/src/flask_app

COPY . ./

RUN adduser -u 8877 newuser -D && chown -R newuser /usr/src/flask_app/

EXPOSE 5000

USER newuser
