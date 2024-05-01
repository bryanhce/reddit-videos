#!/bin/bash

# Run the container passing in the env file, param file and docker image
docker run -v ./parameters.json:/code/parameters.json --env-file .env reddit-videos

# Upon successful generation, extract the video
docker cp $(docker ps -q -n=1):/code/video/output.mp4 ./video/output.mp4
