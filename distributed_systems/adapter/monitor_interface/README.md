# The Adapter Design Pattern
## Commonly used to modify the interface of an existing application, so that it adheres to requirements. In this example, we will apply this design pattern to an existing redis key value store container that doesn't have a proper interface to allow the prometheus monitoring application to scrape information from it. Prometheus expects a /metrics http endpoint to be exposed for every application being monitored, and the redis application doesn't natively provide said interface. This is where the adapter pattern fits in nicely, as we don't have to alter the redis app to enable this interface, we can simply spin up the redis_exporter container, which will sit in between redis and prometheus, and will pull stats from the former and provide to the latter in the required format. To show an alternate and suboptimal approach, we will manually update the flask web application to expose the /metrics interface using a prometheus clienty library. Note that the second approach is less modular, isn't reusable, and is  tightly coupled with the app. In addition, an issue with the prometheus client library and code could negatively impact the application container, so by using the adapter approach one can segregate these duties and prevent a failure with one impacting the other. 

![request splitting architecture diagram](ambassador_request_splitting_arch.png)

## Prerequisites:  
Install the docker engine before proceeding.  

Offical Docker install reference:  
https://docs.docker.com/engine/install  

## Build Procedure:
1. Build docker image for flask production web application:  
  ```shell
  sudo docker build --tag web-app-prod:latest ./app_prod  
  ```
  
2. Run the newly built image:  
  ```shell  
  sudo docker run -d -p 5001:5001 --name web-app-prod web-app-prod   
  ```
  
3. Ensure container is running and send a request to the app to make sure it is responding to requests:  
  ```shell  
  sudo docker ps  
  curl http://localhost:5001  
  ```

4. Build docker image for flask experimental web application:  
  ```shell
  sudo docker build --tag web-app-experiment:latest ./app_experiment
  ```

5. Run the newly built image:  
  ```shell
  sudo docker run -d -p 5002:5002 --name web-app-experiment web-app-experiment   
  ```
  
6. Ensure container is running and send a request to the app to make sure it is responding to requests:   
  ```shell
  sudo docker ps  
  curl http://localhost:5002  
  ```

7. Build docker image for nginx reverse proxy which will act as the ambassador and split requests:  
  ```shell
  sudo docker build --tag nginx-proxy:latest ./proxy 
  ```
  
8. Run the newly built image, and link to the other containers so nginx knows where to proxy requests:  
  ```shell
  sudo docker run -d -p 8080:8080 --link web-app-prod:web-app-prod --link web-app-experiment:web-app-experiment --name nginx-proxy nginx-proxy
  ```
  
9. Ensure container is running and send a request to the app to make sure it is responding to requests:  
  ```shell
  sudo docker ps
  curl http://localhost:8080
  ```
  
10. Nginx is configured to send 90% of requests to the prod app, and 10% to the experimental version. Send 10 requests to the nginx reverse proxy/ambassador, and ensure at least one request is being routed to the experimental web application:
  ```shell
  for i in {1..10}; do
    curl http://localhost:8080 && echo ""
  done 
  ```

