#!/bin/sh

wait-for-it --service $ELASTIC_HOST:$ELASTIC_PORT -t 30 \
            -- python migrate.py
