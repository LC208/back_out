FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /back
COPY req.txt /back/
RUN pip install --upgrade pip && pip install -r req.txt