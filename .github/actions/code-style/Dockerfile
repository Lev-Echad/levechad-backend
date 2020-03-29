FROM python:3.6-alpine

RUN apk add curl jq
RUN pip install pycodestyle

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
