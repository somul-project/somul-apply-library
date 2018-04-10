FROM python:3.6-jessie

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "wsgi.py" ]
