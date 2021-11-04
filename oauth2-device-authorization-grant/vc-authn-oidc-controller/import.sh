#!/bin/sh

echo "Import script... Sleeping for a while..."
sleep 15
echo "Sleep done."

for filename in /import/*.json; do

    echo "Importing $filename..."
    #    -H "X-Api-Key: 12345"\
    curl -X POST "http://127.0.0.1/api/vc-configs"\
        -H "accept: application/json"\
        -H "Content-Type: application/json-patch+json"\
        -d "@$filename"
    echo "done."

done
echo "Importing done."

echo "Setting up database with redirect URIs..."

psql -h controller-db -U controller -d controller -f /import/insert_uri.sql

psql -h controller-db -U controller -d controller -f /import/redirect_uris.sql
