#!/bin/bash

echo "basic test: send 3 requests to test/<1 - 10> endpoint, and examine which shard each unique request uri is being routed to"
for i in {1..10}; do
  echo "Request URI: test/${i}"
  for x in {1..3}; do
    response=$(curl -v http://localhost:8080/test/${i} 2>&1)
    shard=$(echo "$response" | grep X-Backend-Node | cut -d ":" -f2 | tr -d '[:cntrl:]')
    cache_hit=$(echo "$response" | grep X-Cache | cut -d ":" -f2 | tr -d '[:cntrl:]')
    echo "Shard: ${shard}  |  Cache: ${cache_hit}"
  done
  echo ""
done 
 
