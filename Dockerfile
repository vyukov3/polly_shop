FROM python:3.10-bullseye

RUN mkdir /app
WORKDIR /app

RUN pip install "poetry==1.2.2"

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without dev --output /app/requirements.txt

RUN pip install --upgrade pip setuptools wheel \ 
    && pip install --no-cache -r /app/requirements.txt

COPY ./api ./api

EXPOSE 8000

CMD ["uvicorn", "api.__main__:app", "--host", "0.0.0.0", "--port", "8000"]
