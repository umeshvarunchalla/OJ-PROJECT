FROM python:3.12

RUN apt-get update && apt-get install -y gcc g++

WORKDIR /virtual_app

COPY . /virtual_app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=OJ.settings

ENV PYTHONUNBUFFERED=1

CMD ["python","manage.py","runserver","0.0.0.0:8000"]