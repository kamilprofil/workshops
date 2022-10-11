FROM python:3.9.14-slim-bullseye

RUN apt-get update && apt-get install -y \
  curl 

WORKDIR /web
COPY ./requirements.txt /web/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /web/app

HEALTHCHECK CMD curl -f http://localhost/items || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
