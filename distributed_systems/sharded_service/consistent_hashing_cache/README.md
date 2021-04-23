
# setup and initialize environment w/ 4 shards

#1. create symlinks for both docker-compose and nginx
cd consistent_hashing_cache
ln -s 4_shards_docker-compose.yml docker-compose.yml
ln -s 4_shards_nginx.conf nginx.conf

#2. startup all containers via docker-compose
sudo docker-compose up

#3. ensure all containers are running and healthy
sudo docker ps

#4. test out services via pre-built shell script:
./testing.sh

Note where each of the 10 requests are being routed to

#5. remove the current sym link for docker-compose.yml and assign to the 4 sharded one:
rm docker-compose.yml
ln -s 3_shards_docker-compose.yml docker-compose.yml

#6. build and run the new shard (cache and backend containers) without impacting the existing/running ones:
sudo docker-compose up -d --no-recreate --remove-orphans

#7. ensure the new containers have started and the existing containers were NOT restarted
sudo docker ps

#8. remove the current sym link for nginx.conf and assign to the 3 sharded one:
rm nginx.conf
ln -s 3_shards_nginx.conf nginx.conf

#9. restart the nginx contianer without impacting the others
sudo docker-compose restart nginx

#10. ensure the nginx container was restarted and the existing containers were NOT restarted: 
sudo docker ps

#11. run the same test again
./testing.sh 

