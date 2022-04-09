FROM ghcr.io/sibyx/archlinuxarm-docker:master

RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm avahi python python-pip
RUN pip install setuptools

WORKDIR /usr/src/app

COPY . .

RUN python setup.py install
