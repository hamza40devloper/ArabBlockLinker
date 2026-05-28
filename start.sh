#!/bin/bash

set -e

echo "Checking PaperMC..."

if [ ! -f paper.jar ]; then
  echo "Downloading PaperMC..."
  curl -L -o paper.jar "https://fill-data.papermc.io/v1/objects/2c2af90d6ef0e823c272e7059873e3b7a24e07674e56e3b8d6c63ebff03cf827/paper-26.1.2-66.jar"
fi

echo "Starting server..."

java -Xms1G -Xmx2G -jar paper.jar nogui
