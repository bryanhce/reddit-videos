#!/bin/bash

# # Step 1: Navigate to your project directory
# cd /path/to/your/project/directory

# Step 2: Build the image
docker build -t reddit-videos .

# Step 3: Run the container passing in the env file and docker image
docker run --env-file .env reddit-videos

# Step 4: Upon successful generation, extract the video
docker cp $(docker ps -q -n=1):/code/video/output.mp4 ./video/output.mp4
