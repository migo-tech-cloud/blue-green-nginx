#!/bin/sh
envsubst '$ACTIVE_POOL' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf
nginx -g "daemon off;"


