#!/bin/sh

wait-for-it --service http://localhost:8123/ \
            -- python initial.py