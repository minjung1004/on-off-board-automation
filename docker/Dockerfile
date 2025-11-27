FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
	tzdata \
	git \
	vim \
	nano \
	curl \
	wget \
	python3 \
	python3-pip \
	python3-requests \
	python3-yaml \
	python3-jinja2 \
	sudo \
	&& ln -fs /usr/share/zoneinfo/US/Pacific /etc/localtime \
	&& dpkg-reconfigure --frontend noninteractive tzdata \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir -p /workspace

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]
