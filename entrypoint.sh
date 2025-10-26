#!/bin/sh
envsubst '$ACTIVE_POOL' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
nginx -g 'daemon off;'

