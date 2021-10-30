FROM python:3.8.10




RUN pip install typing
RUN pip install pydantic
RUN pip install uvicorn
RUN pip install fastapi
RUN pip install sqlalchemy
RUN pip install mysql-connector-python


COPY ./__init__.py /my-api/__init__.py
COPY ./crud.py /my-api/crud.py
COPY ./app.py /my-api/main.py
COPY ./models.py /my-api/models.py
COPY ./schemas.py /my-api/schemas.py
COPY ./database.py /my-api/database.py


EXPOSE 3306
EXPOSE 8080:80

CMD [ "uvicorn", "my-api.main:app","--reload" ]