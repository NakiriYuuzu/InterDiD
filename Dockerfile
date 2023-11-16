FROM ubuntu:latest
LABEL authors="herry"

ENTRYPOINT ["top", "-b"]