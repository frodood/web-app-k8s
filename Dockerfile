FROM python:3.6.1-alpine
ADD . /usr/src/app

WORKDIR /usr/src/app

RUN set -e; \
	pip install -r requirements.txt;

EXPOSE 80

CMD ["python", "web_app.py"]
