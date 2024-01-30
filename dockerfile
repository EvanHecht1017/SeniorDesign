# Use an older Python image that supports Python 2
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Install pygerber
# You might need to use 'pip2' instead of 'pip' depending on the base image
RUN pip install pygerber

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Command to run on container start
CMD [ "python", "./your-script.py" ]




