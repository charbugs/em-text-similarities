#!/bin/bash

MARKER_NAME=em-text-similarities

cd /home/charbugs/github/$MARKER_NAME/server
uwsgi --pidfile /tmp/$MARKER_NAME.pid \
	--module server:application \
	--master \
	--processes 3 \
	--socket /tmp/$MARKER_NAME.sock \
	--chmod-socket=660 \
	--vacuum \
	--logto /tmp/$MARKER_NAME.log &


