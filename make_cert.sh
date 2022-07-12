#!/usr/bin/env bash

mkdir -p ssl
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -subj "/C=CO/ST=Risaralda/L=Pereira/O=Globomantics/CN=crm.njrusmc.net" -keyout ssl/key.pem -out ssl/cert.pem