#!/usr/bin/env bash
set -e
REPO="madhavsanjaypatil/scientific-calc"
TAG="$(git rev-parse --short HEAD)"
docker build -t ${REPO}:${TAG} .
docker login
docker push ${REPO}:${TAG}
echo "pushed ${REPO}:${TAG}"

