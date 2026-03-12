#!/usr/bin/env bash
set -euo pipefail

mkdir -p certs

openssl req \
  -x509 \
  -newkey rsa:2048 \
  -sha256 \
  -nodes \
  -keyout certs/localhost.key \
  -out certs/localhost.crt \
  -days 365 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

cp certs/localhost.crt certs/ca.pem

echo "Generated: certs/localhost.crt, certs/localhost.key, certs/ca.pem"
