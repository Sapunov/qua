#!/bin/bash

case $1 in

"on" )
        mv /etc/nginx/conf.d/app.conf /etc/nginx/conf.d/app.conf.off
        mv /etc/nginx/conf.d/maintenance.conf.off /etc/nginx/conf.d/maintenance.conf
        nginx -s reload
        echo "Maintenance mode ON"
        ;;
"off" )
        mv /etc/nginx/conf.d/app.conf.off /etc/nginx/conf.d/app.conf
        mv /etc/nginx/conf.d/maintenance.conf /etc/nginx/conf.d/maintenance.conf.off
        nginx -s reload
        echo "Maintenance mode OFF"
        ;;
* )
        echo "Please, say me what to do [on|off]"
        ;;
esac
