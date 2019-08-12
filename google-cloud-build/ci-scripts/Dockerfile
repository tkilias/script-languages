FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN apt-get update && \
    apt-get install -y python3-pip git && \
    apt-get -y clean && \
    apt-get -y autoremove
RUN pip3 install pipenv

COPY --from=buildkite/github-release /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=buildkite/github-release /github-release /bin/github-release

RUN curl -o github-commit-status-1.0.0-linux-amd64.tar.gz  https://github.com/thbishop/github-commit-status/releases/download/1.0.0/github-commit-status-1.0.0-linux-amd64.tar.gz && \
    tar -xvf github-commit-status-1.0.0-linux-amd64.tar.gz && \
    rm github-commit-status-1.0.0-linux-amd64.tar.gz && \
    mv github-commit-status /bin 
