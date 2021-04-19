#!/bin/bash

echo "basic test: send 5 requests to localhost:8080 and ensure first request is a miss and the other 4 are hits"
for i in {1..5}; do
  curl -v http://localhost:8080 2>&1 | grep X-Cache 
done
echo "" 


echo "/time test: send 5 requests to localhost:8080/time and ensure the time returned is unique"
echo "and NOT pulled from cache. Also notice how each request is distributed across the two backends uniformly."
echo "Note: this URL has been explicity excluded in varnish config - default.vcl"
for i in {1..5}; do
  response=$(curl -v http://localhost:8080/time 2>&1)
  echo "$(echo "$response" | grep "Date/Time") | Node: $(echo "$response" | grep X-Backend)"
  sleep 1 
done
echo "" 


echo "/sleep test: send 5 requests to localhost:8080/sleep and ensure the first request takes > 3 seconds."
echo "The last 4 requests take a fraction of the time as they pull directly from cache"
echo "and never interact with the python webapp backend."
for i in {1..5}; do
  request_time=$((time curl http://localhost:8080/sleep) 2>&1 > /dev/null | grep real | awk '{print $2}')
  echo "Request Time: $request_time"
done
