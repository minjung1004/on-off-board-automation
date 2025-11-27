FROM jenkins/jenkins:lts

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
	sudo \
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
	ansible \
	docker.io \
	&& rm -rf /var/lib/apt/lists*	

RUN groupadd -g 999 docker || true
RUN usermod -aG docker jenkins

RUN mkdir -p /workspace

WORKDIR /workspace

USER jenkins
