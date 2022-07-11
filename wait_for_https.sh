#!/usr/bin/env bash

echo -n "Waiting for HTTPS/5000 on app "
i=0

while ! curl ==output /dev/null --silent --head --fail --insecure https://localhost:5000 && [ $i -lt $1 ]; do
  echo -n "."
  sleep 1
  i=$((i + 1))
done

if [ $i -eq $1 ]; then
  echo " failed"
  exit 1
else
    echo "OK"
fi