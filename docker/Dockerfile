FROM jenkins/jenkins:lts

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
	sudo \
	git \
	clean \
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

RUN mkdir -p /workspace
WORKDIR /workspace

ARG DOCKER_GID=125
RUN groupadd -g $DOCKER_GID docker || true
RUN usermod -aG docker jenkins

USER jenkins

EXPOSE 8080 50000 