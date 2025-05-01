#!/bin/sh
# This script is used to start the backend server from docker.
# do not run this file in local

python entrypoint.py
uvicorn backend.backend:app --host 0.0.0.0 --port 8003