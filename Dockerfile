FROM python:3.9.16-bullseye
RUN apt-get update

WORKDIR /

COPY ./exposure_api ./exposure_api
COPY ./setup.py .

RUN pip install flask
RUN python setup.py install

# expose endpoint
EXPOSE 8080

# run
CMD [ "waitress-serve", "--port=8080" , "--call", "exposure_api:create_app"]