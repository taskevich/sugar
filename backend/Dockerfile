FROM python:3.10-buster as builder

ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y

COPY req.txt .
RUN pip3 install -r req.txt
RUN rm req.txt
WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["bash", "-c", "alembic upgrade head && python init.py"]