FROM python:3.6

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


COPY ./__init__.py /my-api/__init__.py
COPY ./crud.py /my-api/crud.py
COPY ./app.py /my-api/app.py
COPY ./models.py /my-api/models.py
COPY ./schemas.py /my-api/schemas.py
COPY ./database.py /my-api/database.py



CMD [ "uvicorn","my-api.app:app --reload" ]
