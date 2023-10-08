#!/bin/sh -ex

celery -A tasks worker -l info
celery -A tasks beat -l info -S django