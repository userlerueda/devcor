#!/usr/bin/env bash

./make_cert.sh
pylint src/*.py
bandit src/*.py --skip B101
pytest src/test_unit.py
docker-compose down --volumes
docker-compose up --build -d
./wait_for_https.sh 60
pytest src/test_system.py