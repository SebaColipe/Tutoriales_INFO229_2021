FROM python:3.8.10

COPY ./my-api /app

ENV BIND_PORT 5000  

WORKDIR /app


RUN pip install typing pydantic uvicorn fastapi sqlalchemy mysql-connector-python


EXPOSE $BIND_PORT

CMD [ "uvicorn","my-api.main:app","--host=0.0.0.0", "--reload" ]
