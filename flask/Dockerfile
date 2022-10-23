FROM python:3.9-alpine

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /code

ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD ./application.py .
ADD ./home_budget ./home_budget

EXPOSE 5000
CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "application"]