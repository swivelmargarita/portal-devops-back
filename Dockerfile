FROM python:3.10-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
COPY  requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.10-slim AS build-image
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /django
COPY accounts config main manage.py ./
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
