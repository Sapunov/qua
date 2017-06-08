FROM qua-ubuntu:16.04

COPY conf/qua-api.conf /etc/nginx/sites-available/
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY src /var/www/qua-api
COPY qua_common /tmp/qua_common

RUN mkdir -p /var/lib/qua/data/static /var/log/qua \
	&& rm /etc/nginx/sites-enabled/default \
	&& ln -s /etc/nginx/sites-available/qua-api.conf /etc/nginx/sites-enabled/qua-api.conf \
	&& echo "daemon off;" >> /etc/nginx/nginx.conf \
	&& pip3 install --no-cache-dir -r /var/www/qua-api/requirements.txt \
	&& cd /tmp/qua_common \
	&& python3 /tmp/qua_common/setup.py install --skip-build \
	&& chown -R www-data:www-data /var/www/qua-api /var/lib/qua /var/log/qua

VOLUME /var/lib/qua/data

WORKDIR /var/www/qua-api

RUN nginx -t \
	&& python3 -c 'import compileall, os; compileall.compile_dir(os.curdir, force=1)' > /dev/null \
	&& ./manage.py collectstatic --settings=app.settings --no-input -v0

CMD ["/usr/bin/supervisord"]
