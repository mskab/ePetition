FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --system --clear

COPY . ./

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
