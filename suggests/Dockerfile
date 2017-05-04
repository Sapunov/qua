FROM qua-ubuntu:16.04

COPY conf/qua-suggests.conf /etc/nginx/sites-available/
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY src /var/www/qua-suggests
COPY qua_common /tmp/qua_common

RUN mkdir -p /var/lib/qua/data/ /var/log/qua \
	&& rm /etc/nginx/sites-enabled/default \
	&& ln -s /etc/nginx/sites-available/qua-suggests.conf /etc/nginx/sites-enabled/qua-suggests.conf \
	&& echo "daemon off;" >> /etc/nginx/nginx.conf \
	&& pip3 install -r /var/www/qua-suggests/requirements.txt \
	&& cd /tmp/qua_common && make \
	&& rm -rf /tmp/qua_common \
	&& chown -R www-data:www-data /var/www/qua-suggests /var/lib/qua /var/log/qua

VOLUME /var/lib/qua/data

CMD ["/usr/bin/supervisord"]
