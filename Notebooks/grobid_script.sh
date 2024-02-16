#!/bin/bash

# Step 1: Pull the Grobid Docker image
docker pull grobid/grobid:0.7.1

# Step 2: Run the Grobid Docker container in the background
docker run -d --rm --name grobid -p 8070:8070 -p 8071:8071 grobid/grobid:0.7.1

# Wait a bit for the container to initialize (Grobid needs some time to start)
echo "Waiting for Grobid to start..."
sleep 30 # Adjust this based on your system's performance

# Define the base path for the input files (adapt this path to where your script and files are located)
BASEPATH="/Users/shubh/Downloads/Archive 2 (1)"

# Step 3: Process files with Grobid and save the output
echo "Processing Level I..."
curl -v --form input=@"${BASEPATH}/2024-l1-topics-combined-2.pdf" http://localhost:8070/api/processFulltextDocument > Grobid_RR_2024_LevelI_combined.xml

echo "Processing Level II..."
curl -v --form input=@"${BASEPATH}/2024-l2-topics-combined-2.pdf" http://localhost:8070/api/processFulltextDocument > Grobid_RR_2024_LevelII_combined.xml

echo "Processing Level III..."
curl -v --form input=@"${BASEPATH}/2024-l3-topics-combined-2.pdf" http://localhost:8070/api/processFulltextDocument > Grobid_RR_2024_LevelIII_combined.xml

# Stop the Grobid container
docker stop grobid

echo "Processing completed."
