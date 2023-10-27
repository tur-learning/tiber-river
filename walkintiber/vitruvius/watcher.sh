#!/bin/bash

# Directory where .osm files are located
DATA_DIR="/app/data"

# Directory where processed files are to be moved
PROCESSED_DIR="/app/data/processed"

# Create the processed directory if it does not exist
mkdir -p "$PROCESSED_DIR"

# Start the inotifywait loop, watching for new files created or moved in the data directory
# The -e close_write option is used to capture the event when files created or modified
# The --format option specifies that only the filename should be output
inotifywait -m "$DATA_DIR" -e create -e moved_to --format '%w%f' --excludei '\.(obj)$' | while read FILEPATH
do
  # Extract just the filename from the full path
  FILENAME=$(basename "$FILEPATH")

  # Check if the modified file is an .osm file
  if [[ "$FILENAME" == *.osm ]]; then
    echo "Detected new .osm file '$FILENAME' for processing."

    # Full paths for the input and output files
    INPUT_FILE="$FILEPATH"
    OUTPUT_FILE="${FILENAME%.osm}.obj"  # Change extension to .obj

    # Run the OSM2World command
    ./osm2world/osm2world.sh -i "$INPUT_FILE" -o "$DATA_DIR/$OUTPUT_FILE"

    # If OSM2World command was successful, move the .osm file to the processed directory
    if [ $? -eq 0 ]; then
      echo "Processing completed for '$FILENAME'. Moving to 'processed' directory."
      mv "$INPUT_FILE" "$PROCESSED_DIR/"
    else
      echo "An error occurred during processing. '$FILENAME' will remain in '$DATA_DIR'."
    fi
  fi
done
