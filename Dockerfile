FROM jenkins/jenkins:latest
USER root
WORKDIR /my_app
RUN pwd
RUN ls -la
RUN apt-get update
RUN apt-get install -y python3-pip
