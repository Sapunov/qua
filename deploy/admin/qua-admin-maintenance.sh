#!/bin/bash


CONF_FILE=/etc/nginx/conf.d/app.conf
MAINTENANCE_FILE=/etc/nginx/conf.d/maintenance.conf


case $1 in

"on" )
	if [ -e $CONF_FILE ] && [ -e "$MAINTENANCE_FILE.off" ]
		then
			if mv $CONF_FILE "$CONF_FILE.off" \
				&& mv "$MAINTENANCE_FILE.off" $MAINTENANCE_FILE \
				&& nginx -t
			then
			systemctl restart nginx && echo "Maintenance mode ON"
			fi
		else
			echo "Maintenance mode already ON"
		fi
	;;
"off" )
	if [ -e "$CONF_FILE.off" ] && [ -e $MAINTENANCE_FILE ]
		then
			if mv "$CONF_FILE.off" $CONF_FILE \
				&& mv $MAINTENANCE_FILE "$MAINTENANCE_FILE.off" \
			&& nginx -t
			then
			systemctl restart nginx && echo "Maintenance mode OFF"
			fi
		else
			echo "Maintenance mode already OFF"
		fi
	;;
* )
	echo "Please, say me what to do [on|off]"
	;;
esac
