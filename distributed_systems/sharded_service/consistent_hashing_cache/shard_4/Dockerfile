# use python offical image from dockerhub as base image for this container
FROM python 

# copy contents of this directory to the /app directory within the container
COPY . /app

# set working directory of container
WORKDIR /app

# install the python prerequisites using the requirements.txt file
RUN pip install -r requirements.txt

# set the port the container will listen for requests on to 5001
EXPOSE 5004

# use python to execute the flask web application
ENTRYPOINT [ "python" ]
CMD [ "web_app_4.py" ]

