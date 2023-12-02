#!/bin/bash 

uvicorn src.main:app --host 0.0.0.0 --port $AUTH_PORT --reload --log-level debug
# gunicorn src.main:app -k uvicorn.workers.UvicornWorker --reload --bind 0.0.0.0:$AUTH_PORT