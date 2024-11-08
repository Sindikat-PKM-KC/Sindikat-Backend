FROM python:latest

RUN pip install --upgrade pip

COPY ./project/requirement.txt .
RUN pip install -r requirement.txt

COPY ./project /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
