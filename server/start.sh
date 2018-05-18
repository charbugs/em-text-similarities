#!/bin/bash

MARKER_NAME=em-text-similarities

cd ~/github/$MARKER_NAME/server
sudo ~/.local/bin/uwsgi \
	--pidfile /tmp/$MARKER_NAME.pid \
	--module server:application \
	--master \
	--processes 3 \
	--socket /tmp/$MARKER_NAME.sock \
	--chmod-socket=666 \
	--vacuum \
	--logto /tmp/$MARKER_NAME.log &


