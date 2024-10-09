FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
  gcc \
  musl-dev \
  postgresql-dev \
  libpq \
  bash

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]