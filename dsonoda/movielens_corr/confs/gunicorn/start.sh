#!/bin/bash

WORKING_DIR="/home/ubuntu/pycamp-20170603/dsonoda/movielens_corr/movielens_corr"
ACTIVATE_PATH="/home/ubuntu/venv/bin/activate"

cd ${WORKING_DIR}
source ${ACTIVATE_PATH}

exec gunicorn movielens_corr.wsgi -b unix:${WORKING_DIR}/gunicorn.sock
