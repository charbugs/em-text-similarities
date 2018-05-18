#!/bin/bash

MARKER_NAME=em-text-similarities

cd ~/github/$MARKER_NAME/server
sudo ~/.local/bin/uwsgi \
	--stop /tmp/$MARKER_NAME.pid
