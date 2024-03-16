#!/bin/bash

echo "Creating indexes"
curl -s -XPUT -H 'Content-Type: application/json' -d @/data/indexes/movies.json http://elasticsearch:9200/movies
curl -s -XPUT -H 'Content-Type: application/json' -d @/data/indexes/genres.json http://elasticsearch:9200/genres
