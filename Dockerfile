# syntax = docker/dockerfile:1.2

FROM python:3

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      texlive-latex-extra \
	  texlive-fonts-recommended \
	  texlive-plain-generic \
	  dvipng

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY distex.py .

CMD [ "python", "./distex.py" ]
