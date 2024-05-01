#!/bin/bash

# only run this file when you made edits to the code

# # Step 1: Build the image
docker build -t reddit-videos .

# Step 2: Run the container passing in the env file and docker image
docker run -v ./parameters.json:/code/parameters.json --env-file .env reddit-videos

# Step 3: Upon successful generation, extract the video
docker cp $(docker ps -q -n=1):/code/video/output.mp4 ./video/output.mp4