# use nginx offical image from dockerhub as base image for this container
FROM nginx 

# copy custom nginx.conf to /etc/nginx inside of container
COPY nginx.conf /etc/nginx/nginx.conf 

# set the port the container will listen for requests on to 8080 
EXPOSE 8080 

