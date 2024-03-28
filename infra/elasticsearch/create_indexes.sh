#!/bin/bash

ELASTICSEARCH_URL=$1

echo "Creating indexes at Elasticsearch: $ELASTICSEARCH_URL"
curl -s -XPUT -H 'Content-Type: application/json' -d @/data/indexes/movies.json "$ELASTICSEARCH_URL"/movies
curl -s -XPUT -H 'Content-Type: application/json' -d @/data/indexes/genres.json "$ELASTICSEARCH_URL"/genres
curl -s -XPUT -H 'Content-Type: application/json' -d @/data/indexes/persons.json "$ELASTICSEARCH_URL"/persons
