

FROM python:3.11.5

WORKDIR /opt/ContentClassifier

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
#RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install -r requirements.txt


