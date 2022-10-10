FROM python:3.8.5

WORKDIR /code
COPY . .
RUN pip install requirements.txt
CMD ["gunicorn", "foodgram_api.wsgi:application", "--bind", "0.0.0.0:8000"]