#!/bin/bash

echo "Import script... Sleeping for a while..."
#sleep 15
echo "Sleep done."

for filename in /import/*.json; do

    # this loop tries to run as long as necessary to get a successful response from the API
    # it may take a while until the API is up and running
    while true ; do
        echo "Importing $filename..."
        #    -H "X-Api-Key: 12345"\
        http_code=$( curl --silent --show-error --fail --write-out '%{http_code}' -X POST "http://127.0.0.1/api/vc-configs"\
            -H "accept: application/json"\
            -H "Content-Type: application/json-patch+json"\
            -d "@$filename" )
        echo "http_code: "
        # 000 is connection refused values here
        echo $http_code
        if [[ $http_code -eq 400 ]]; then
            echo "400 indicates that we have already successfully uploaded our config once (in the previous run)"
            echo "Configuration import sucessfully finished."
            break
        fi
        echo "done."
        sleep 2
    done

done
echo "Importing done."
