#!/bin/bash

for payload in $(jq '.[]' -c test.scenarios.json); do
  curl -X 'POST' -H 'accept: application/json' -H 'Content-Type: application/json' -d $payload 'http://localhost:8000/scenario?recalculate_time=true'
  sleep $(( RANDOM % 5 ))
done
