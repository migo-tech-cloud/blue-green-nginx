#!/bin/sh
envsubst '$ACTIVE_POOL' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf
nginx -s reload
