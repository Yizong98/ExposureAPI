# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.7-buster

WORKDIR /

COPY ./exposure_api ./exposure_api
COPY ./setup.py .
COPY ./instance/google_credentials.json /usr/local/var/exposure_api-instance/google_credentials.json

# Builds production wheel file and removes source code.
RUN python setup.py bdist_wheel && rm -rf exposure_api && pip install ./dist/exposureAPI-1.0.0-py3-none-any.whl

CMD [ "waitress-serve", "--port=8080" , "--call", "exposure_api:create_app"]