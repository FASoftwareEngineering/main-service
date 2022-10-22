FROM python:3.9.6-alpine AS builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev build-base libffi-dev

RUN pip install --upgrade pip
COPY app .

RUN apk add --no-cache libressl-dev musl-dev libffi-dev gcc
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


FROM python:3.9.6-alpine AS build

# Setup the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME && addgroup -S app && adduser -S app -G app
RUN mkdir $APP_HOME/staticfiles && mkdir $APP_HOME/mediafiles

WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq gcc musl-dev libffi-dev
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt ./
RUN pip install --no-cache /wheels/*

COPY app $APP_HOME
RUN chown -R app:app $APP_HOME

USER app

CMD ["python3", "main.py"]