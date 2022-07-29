# dockerfile for hashtopocli

# build stage
FROM python:slim AS build
ENV PATH="/opt/venv/bin":$PATH
WORKDIR /opt
RUN apt-get update; apt-get install -y git python3 pip curl; rm -rf /var/lib/apt/lists/*; python3 -m pip install virtualenv; \
    virtualenv -p python venv; PATH="/opt/venv/bin:$PATH";\
    git clone https://github.com/JakeWnuk/HashtopoCLI; pip3 install -r /opt/HashtopoCLI/requirements.txt; \
    mv /opt/HashtopoCLI/hashtopocli.py /opt/venv/bin/hashtopocli.py; chmod +x /opt/venv/bin/hashtopocli.py

# final stage
FROM python:slim
COPY --from=build /opt/venv /opt/venv
ADD ./config.yml /opt/venv/bin/config.yml
ENV PATH="/opt/venv/bin:$PATH"
RUN apt-get update; apt-get install -y tini; rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/bin/tini", "--","/opt/venv/bin/hashtopocli.py"]
