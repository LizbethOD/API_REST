FROM ubuntu:20.04
RUN apt-get install -y
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install sqlite3 -y
RUN pip install Pyrebase4
RUN pip3 install pytest
RUN pip3 install requests

ENV requirements /home/requirements.txt

COPY requirements.txt ${requirements}

RUN pip3 install -r /home/requirements.txt

WORKDIR /home/