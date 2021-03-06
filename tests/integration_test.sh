#!/bin/bash
# integration-tests.sh
echo "Starting integration tests..."
# check the request response code on /homersimpson
res1=$(curl -s -o /dev/null -w "%{http_code}" http://$1/homersimpson/)

if [ "$res1" != "200" ]; then
 echo "Path /homersimpson test failed. Aborting..."
 exit 1
fi
# check the request response code on /covilha
res2=$(curl -s -o /dev/null -w "%{http_code}" http://$1/covilha/)
if [ "$res2" != "200" ]; then
 echo "Path /covilha test failed. Aborting..."
 exit 1
fi

echo "Integration tests succeeded."
