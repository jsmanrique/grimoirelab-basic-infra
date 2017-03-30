FROM python:3.4-slim

MAINTAINER J. Manrique López <jsmanrique@gmail.com>

ADD src/grimoire-demo.py /

RUN pip install perceval
RUN pip install grimoire-elk
RUN pip install PyYAML
RUN pip install github3.py

RUN apt-get update && \
  apt-get install -y git

# VOLUME settings/data-sources.yml /settings/data-sources.yml

CMD ["python", "./grimoire-demo.py"]
