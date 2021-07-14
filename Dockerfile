FROM python:3.8-slim-buster

RUN mkdir /mlhportfolio_v2
COPY requirements.txt /mlhportfolio_v2
WORKDIR /mlhportfolio_v2
RUN pip3 install -r requirements.txt

COPY . /mlhportfolio_v2

# CMD ["gunicorn", "wsgi:app", "-w 4", "-b 0.0.0.0:80"]
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["sh" , "./entrypoint.sh"]