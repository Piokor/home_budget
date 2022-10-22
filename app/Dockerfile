FROM node:12.2.0-alpine as build-vue

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY vue/package.json /app/package.json
RUN npm install
COPY vue .
RUN npm run build

FROM python:3.9-alpine

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /code

ADD home_budget/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD . .
COPY --from=build-vue /app/dist /code/home_budget/templates/dist

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000
CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "application"]