FROM python:3.6
MAINTAINER XenonStack

# Creating Application Source Code Directory
RUN mkdir -p /usr/src/app

# Setting Home Directory for containers
WORKDIR /usr/src/app

# Installing python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# Copying src code to Container
COPY . /usr/src/app

# Application Environment variables
ENV APP_ENV development

# Exposing Ports
EXPOSE 6379

# Running Python Application
CMD ["python", "./main.py" ]