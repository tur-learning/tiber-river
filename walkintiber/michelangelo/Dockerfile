# Start from the Blender container
FROM nytimes/blender:3.3.1-cpu-ubuntu18.04

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install inotify-tools to enable file system watch
RUN apt-get update && apt-get install -y inotify-tools

# Our start-up script
ENTRYPOINT ["./watcher.sh"]