FROM python:3.7

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /py-nudec

COPY . .

RUN apt update -y
# Install `make` and `pipenv`
RUN apt install build-essential pipenv -y

# Default flask
EXPOSE 5000

# Start
CMD [ "make", "run" ]
