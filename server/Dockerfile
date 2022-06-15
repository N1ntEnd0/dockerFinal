FROM python:3.8.5 as builder

WORKDIR /usr/src/ShareMyGDrive

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

COPY ./requirements.txt .


FROM python:3.8.5

RUN mkdir -p /home/app

#создаем нового пользователя
RUN groupadd app
RUN useradd -m -g app app -p PASSWORD
RUN usermod -aG app app

#создаем рабочую директорию для пользователя
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME

#new
#RUN mkdir $APP_HOME/staticfiles

WORKDIR $APP_HOME

RUN apt-get update

COPY --from=builder /usr/src/ShareMyGDrive/. .
COPY --from=builder /usr/src/ShareMyGDrive/requirements.txt .
#RUN pip install --no-cache ./*
RUN pip install -r requirements.txt

COPY . $APP_HOME

RUN chown -R app:app $APP_HOME

USER app



#EXPOSE 8000
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#EXPOSE 8000
#RUN ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
