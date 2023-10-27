# Start with a base image containing Java runtime (JRE 17)
# FROM openjdk:17-jre-slim
# FROM openjdk:11-ea-17-jre-slim
FROM debian:stable-slim

# Make a directory in the image
WORKDIR /app

# Download OSM2World, extract it, and clean up the downloaded file
ADD https://osm2world.org/download/files/0.3.1/OSM2World-0.3.1-bin.zip /app/osm2world.zip

# Install inotify-tools, bsdtar instead of unzip, JRE
RUN apt-get update && \
    apt-get install -y inotify-tools && \
    apt-get install -y unzip && \
    unzip /app/osm2world.zip -d /app/osm2world && \
    apt-get install -y default-jre && \
    rm /app/osm2world.zip && \
    apt-get remove -y unzip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the watcher script into the image
COPY watcher.sh /app/watcher.sh
# Make sure the script is executable
RUN chmod +x /app/watcher.sh

# Expose the port the app runs on (if your Java application has a web server)
# EXPOSE 8080 # TODO does osm2world have a web server?

# # Command to keep the container running
# CMD ["tail", "-f", "/dev/null"]
# Command to run the watcher script
CMD ["/app/watcher.sh"]
