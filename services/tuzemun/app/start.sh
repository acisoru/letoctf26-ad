#!/bin/bash

while ! nc -z $(echo $POSTGRES_HOST) 5432; do sleep 3; done
echo "Postgres started"

#node index.js
npm start --host 0.0.0.0
