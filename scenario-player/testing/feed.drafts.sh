#!/bin/bash

for payload in $(jq '.[]' -c test_drafts.json); do
  curl -X 'POST' -H 'accept: application/json' -H 'Content-Type: application/json' -d $payload 'http://localhost:8000/scenario_draft'
  sleep $(( RANDOM % 5 ))
done
