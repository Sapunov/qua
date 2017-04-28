FROM qua-ubuntu:16.04

COPY conf/app.conf /etc/nginx/sites-available/
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY conf/django_key /root/django_key
COPY conf/db_password /root/db_password

COPY app /var/www/app/

RUN mkdir -p /var/lib/qua/data/static /var/lib/qua/data/cache /var/log/qua \
	&& rm /etc/nginx/sites-enabled/default \
	&& ln -s /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/app.conf \
	&& echo "daemon off;" >> /etc/nginx/nginx.conf \
	&& pip3 install -r /var/www/app/requirements.txt \
	&& chown -R www-data:www-data /var/www/app \
	&& sed -i "s/DEBUG = True/DEBUG = False/g" /var/www/app/qua/settings.py \
	&& sed -i "s/somestrongdjangokey/$(cat /root/django_key)/g" /var/www/app/qua/settings.py \
	&& sed -i "s/somestrongdbpassword/$(cat /root/db_password)/g" /var/www/app/qua/settings.py

VOLUME /var/lib/qua/data

CMD ["/usr/bin/supervisord"]
