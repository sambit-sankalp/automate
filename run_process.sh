#!/bin/bash

# Define paths and variables
DATA_SCRAPING_SCRIPT="./scrape_data.py"  # Path to your data scraping script
JSON_FILE="newminer.json"  # Path to your JSON file
DOCKER_IMAGE="reputation"  # Name of your Docker image
CONTAINER_JSON_PATH="/app/newminer.json"  # Path inside the container where JSON file will be mounted
DOCKER_REGISTRY="sambitsankalp/bacalhumdemo"  # Your Docker Hub username or registry URL
DOCKER_TAG="latestreputation"  # Tag for your Docker image

# Step 1: Run the data scraping script (optional)
# Uncomment the following line if you need to run a data scraping script

echo "Please enter the address of the miner:"
read address

echo $address

python3 $DATA_SCRAPING_SCRIPT $address


# Step 2: Check if JSON file exists
if [ ! -f "$JSON_FILE" ]; then
    echo "JSON file not found: $JSON_FILE"
    exit 1
fi

Address=$(jq -r '.Address' $JSON_FILE)
AdjustedPower=$(jq -r '.AdjustedPower' $JSON_FILE)
WinCount=$(jq -r '.WinCount' $JSON_FILE)
SectorTotal=$(jq -r '.SectorTotal' $JSON_FILE)
SectorActive=$(jq -r '.SectorActive' $JSON_FILE)
SectorFaults=$(jq -r '.SectorFaults' $JSON_FILE)
SectorRecoveries=$(jq -r '.SectorRecoveries' $JSON_FILE)

echo $Address
echo $AdjustedPower
echo $WinCount
echo $SectorTotal
echo $SectorActive
echo $SectorFaults
echo $SectorRecoveries

# Step 3: Build the Docker image (optional)
# Uncomment the following lines if you need to build your Docker image
# echo "Building Docker image..."
# docker build -t $DOCKER_IMAGE .

# # Step 4: Run the Docker container with the JSON file mounted
# echo "Running Docker container..."
# docker run -v $JSON_FILE:$CONTAINER_JSON_PATH $DOCKER_IMAGE python /app/model.py /app/newminer.json

# echo "Pushing the Docker image to resistry..."
# docker buildx build --platform linux/amd64 --push -t $DOCKER_REGISTRY:$DOCKER_TAG .

# # Get token for Docker Hub
# TOKEN=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$DOCKER_REGISTRY:pull" | jq -r .token)

# # Get the digest
# DIGEST=$(curl -s -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.docker.distribution.manifest.v2+json" "https://registry-1.docker.io/v2/$DOCKER_REGISTRY/manifests/$DOCKER_TAG" | jq -r '.config.digest')

# echo "Digest for $DOCKER_IMAGE:$DOCKER_TAG is $DIGEST"

# # Check if the Docker command was successful
# if [ $? -ne 0 ]; then
#     echo "Failed to run Docker container."
#     exit 1
# fi

echo "Process completed successfully."
