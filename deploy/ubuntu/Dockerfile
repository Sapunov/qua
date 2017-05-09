FROM ubuntu:16.04

MAINTAINER Sapunov Nikita

RUN export LANG=en_US.UTF-8 \
	&& export LANGUAGE=en_US:en \
	&& LC_ALL=en_US:en \

	&& sed -i 's,http://archive.ubuntu.com/ubuntu/,mirror://mirrors.ubuntu.com/mirrors.txt,' /etc/apt/sources.list \
	&& apt-get update -qq \
	&& apt-get upgrade -qq \

	&& apt-get install -y apt-utils \
	&& apt-get purge -y locales \
	&& apt-get install -y locales \
	&& locale-gen en_US.UTF-8 \

	&& apt-get install -y --no-install-recommends \
		python \
		python3 \
		python3-pip \
		python3-setuptools \
		nginx \
		supervisor \
		uwsgi-plugin-python3 \
		vim \

	&& BUILD_DEPS='build-essential python3-dev' \
	&& apt-get install -y --no-install-recommends ${BUILD_DEPS} \

	&& pip3 install --no-cache-dir -U pip uwsgi \
	&& pip3 install --no-cache-dir \
		Django==1.11 \
		django-redis==4.8.0 \
		django-rq==0.9.5 \
		djangorestframework==3.6.2 \
		djangorestframework-jwt==1.10.0 \
		psycopg2==2.7.1 \
		PyJWT==1.5.0 \
		redis==2.10.5 \
		requests==2.13.0 \
		rq==0.7.1 \
		rq-scheduler==0.7.0 \
		elasticsearch==5.3.0 \
		lxml==3.7.3 \
		urllib3==1.21.1 \

	&& apt-get autoremove -y ${BUILD_DEPS} \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
