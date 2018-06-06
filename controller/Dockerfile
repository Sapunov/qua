FROM qua-ubuntu:16.04

COPY conf/qua-controller.conf /etc/nginx/sites-available/
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY src /var/www/qua-controller

RUN mkdir -p /var/lib/qua/data/static /var/log/qua \
	&& rm /etc/nginx/sites-enabled/default \
	&& ln -s /etc/nginx/sites-available/qua-controller.conf /etc/nginx/sites-enabled/qua-controller.conf \
	&& echo "daemon off;" >> /etc/nginx/nginx.conf \

	&& BUILD_DEPS='build-essential python3-dev' \
	&& apt-get update && apt-get install -y --no-install-recommends ${BUILD_DEPS} \

	&& pip3 install --no-cache-dir -I -r /var/www/qua-controller/requirements.txt \
	&& chown -R www-data:www-data /var/www/qua-controller /var/lib/qua /var/log/qua \

	&& apt-get autoremove -y ${BUILD_DEPS} \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY conf/effective_tld_names.dat /var/lib/qua/data/

VOLUME /var/lib/qua/data

WORKDIR /var/www/qua-controller

RUN nginx -t \
	&& python3 -c 'import compileall, os; compileall.compile_dir(os.curdir, force=1)' > /dev/null

CMD ["/usr/bin/supervisord"]
