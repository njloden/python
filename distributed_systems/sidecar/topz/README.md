# The sidecar design pattern is used to augment or compliment an existing application by running an additional application along side of it. The example provided here allows one to run a topz system utilization container along with an existing web application to get a view of the running processes and the resources they are consuming via a simple web interface. 

## Prerequisites:
Install the docker engine before proceeding.

## Offical Docker install reference:
https://docs.docker.com/engine/install

###1. Build docker image for simple flask web application
sudo docker build --tag flask-web-app:latest .

###2. Run the newly built image
sudo docker run -d -p 5001:5001 flask-web-app

###3. Ensure container is running and send a request to the app to make sure it is responding to requests.
sudo docker ps
curl http://localhost:5001

###4. Determine the container ID of the flask-web-app
CONTAINER=flask-web-app
CONTAINER_ID=$(sudo docker ps | grep $CONTAINER | grep -v grep | awk '{print $1}')
echo $CONTAINER_ID 

###5. Pull the topz container from the docker registry, run on port 8001, and run it in the same process id (PID) namespace so it will be able to extract resource metrics for the web application container:
sudo docker run -d --pid=container:${CONTAINER_ID} -p 8080:8080 brendanburns/topz:db0fa58 /server --addr=0.0.0.0:8080

###6. Run the following curl command to get a list of all running processes in the web app container and their respective resource utilizations:
curl http://localhost:8080/topz


