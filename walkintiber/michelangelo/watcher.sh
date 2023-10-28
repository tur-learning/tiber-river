#!/bin/bash

# Directory to watch for changes
WATCH_DIR="/app/data/build"

# Directory where rendered files are to be moved
PROCESSED_DIR="/app/data/render"

# Create the processed directory if it does not exist
if [ ! -d "$PROCESSED_DIR" ]; then
  echo "$(date): Directory $PROCESSED_DIR does not exist. Creating..."
  mkdir -p "$PROCESSED_DIR"
fi

# Check if you can access the directory and it's writable (important for moving files)
if [ ! -w "$PROCESSED_DIR" ]; then
  echo "$(date): Cannot write to $PROCESSED_DIR. Check permissions."
  exit 1
fi

# Function to handle processing of each file
convert_to_glft() {
  # Full paths for the input file and the Blender script
  OBJ_FILE=$1
  FILEPATH="$WATCH_DIR/$OBJ_FILE"  
  SCRIPTPATH="/app/blender_gltf_converter.py"

  echo "$(date): Processing $OBJ_FILE..."
  
  # Run Blender with the provided script and input file. Capture if it's successful.
  blender -b --python "$SCRIPTPATH" -- -mp "$FILEPATH"
  
  # Check if the Blender command was successful
  if [ $? -eq 0 ]; then
    echo "$(date): File '$OBJ_FILE' processed successfully."
    # Construct the name of the output .gltf file based on the original filename
    # Assuming the .gltf file has the same name but with .gltf extension
    # GLTF_FILE="${FILE%.obj}.gltf"
    # Define your base file name by stripping the .obj extension
    BASE_FILENAME="${OBJ_FILE%.obj}"
    # Check if a .gltf or .glb file exists in the WATCH_DIR with the base name
    if [[ -f "${WATCH_DIR}/${BASE_FILENAME}.gltf" ]]; then
        GLTF_FILE="${BASE_FILENAME}.gltf"
    elif [[ -f "${WATCH_DIR}/${BASE_FILENAME}.glb" ]]; then
        GLTF_FILE="${BASE_FILENAME}.glb"
    else
        echo "$(date): No corresponding .gltf or .glb file found for $OBJ_FILE."
        # Handle the case where neither file is present, if necessary.
        # For example, you might want to set a default or exit with an error.
    fi
    # checking if the file exists and is not empty.
    if [ ! -s "$WATCH_DIR/$GLTF_FILE" ]; then
        echo "$(date): File $GLTF_FILE is missing or empty."
        # Handle error, retry, or skip
    else
        # Move the .obj and .gltf files to the rendered directory
        echo "$(date): Attempting to move $OBJ_FILE and $GLTF_FILE to $PROCESSED_DIR"
        mv "$FILEPATH" "$PROCESSED_DIR/"
        mv "$WATCH_DIR/$GLTF_FILE" "$PROCESSED_DIR/"
        echo "$(date): Moved '$OBJ_FILE' and '$GLTF_FILE' to $PROCESSED_DIR"
    fi 
  else
    echo "$(date): An error occurred processing '$OBJ_FILE'. It remains in $WATCH_DIR"
    # Handle the error accordingly
  fi
}

# Start inotifywait loop. This will block until a file is created or moved into the watch directory.
while true; do
    # Wait for a new file to be added or moved to the watch directory and ensure it's a .obj file.
    # Note: The following line might be quite packed, it's configuring inotifywait to wait for 'create' and 'moved_to' events, output the event and filename, and exclude files not ending in .obj.

    # Print a message before waiting for events.
    echo "$(date): Waiting for new events..."

    # Capture the raw output from inotifywait.
    RAW_OUTPUT=$(inotifywait -e create -e moved_to --format '%e %f' "$WATCH_DIR")
    # Check if the output matches the expected .obj files.
    EVENT_OUTPUT=$(echo "$RAW_OUTPUT" | grep -E '\.obj$')

    # Parsing the output to extract the event type and file name.
    # The file name may be empty if the event type is MOVED_TO.
    IFS=' ' read -r EVENT_TYPE FILENAME <<< "$EVENT_OUTPUT"

    if [[ -z "$FILENAME" ]] || [[ -z "$EVENT_TYPE" ]]; then
        echo "$(date): The operation '$RAW_OUTPUT' was detected, but some others might be missing (maybe due to a bulk move operation). Retrying..."
        # You might need additional logic here to handle retries or to check the directory's state.
        # continue

        # # This issue is a common one with file system watchers, especially when multiple files are moved almost simultaneously 
        # # or within the watch cycle of the script: if events happen very quickly and especially in bulk (moving multiple files at once), 
        # # some events might not be captured (inotifywait misses some events during a batch file move).
        # # To handle multiple files moved at the same time, waits to allow any subsequent quick file moves to complete, therefore loop over all 
        # # new files in the directory after each file system event notification, rather than processing just one file per notification:
        # # to processes all .obj files in the directory, not just the one that triggered the most recent event.

        # # This holds the timestamp of the last processed event.
        # last_event_time=0

        # while true; do
        #     # Wait for a new event to occur.
        #     echo "Waiting for new events..."
        #     inotifywait -e create -e moved_to "$WATCH_DIR"
            
        #     # A small delay can help in batch processing if files are moved in quick succession.
        #     sleep 0.5  # This delay can be adjusted based on your specific needs.
            
        #     # Get the current time as a way of processing batches of files.
        #     current_event_time=$(date +%s)
            
        #     # If the events are too close together, they are part of the same batch.
        #     if (( current_event_time - last_event_time < 2 )); then  # '2' is an arbitrary threshold for deciding 'simultaneous' events.
        #         echo "Skipping as these are simultaneous events."
        #         continue
        #     fi

        #     # Update the last event time to the current event.
        #     last_event_time=$current_event_time

        #     # Now, instead of processing a single file, we loop through all files that have just arrived.
        #     for file in "$WATCH_DIR"/*.obj; do
        #         [ -e "$file" ] || continue  # If no files are present, skip the loop.

        #         # Extract just the filename from the path.
        #         filename=$(basename -- "$file")

        #         echo "Processing $filename..."

        #         # Place your file processing commands here.
        #         # For example:
        #         # blender -b "$file" -o "//output" -a
        #         # mv "$file" "/path/to/processed/"

        #         echo "$filename processed."
        #     done
        # done
    fi

    # Check if the event is related to a .obj file.
    if [[ "$EVENT_TYPE" == *"CREATE"* || "$EVENT_TYPE" == *"MOVED_TO"* ]] && [[ "$FILENAME" == *.obj ]]; then
        echo "$(date): Detected new .obj file '$FILENAME', starting processing..."
        convert_to_glft "$FILENAME"
    else
        echo "$(date): A new '$RAW_OUTPUT' event was catched, but it was not the right one ..."
        OBJ_FILES=($(find "$WATCH_DIR" -maxdepth 1 -type f -name "*.obj"))
        # If there are any .obj files, process them
        if [ ${#OBJ_FILES[@]} -gt 0 ]; then
            for file in "${OBJ_FILES[@]}"; do
            # Extract just the filename from the path
            FILENAME=$(basename "$file")
            echo "$(date): Detected new .obj file '$FILENAME', starting processing..."
            convert_to_glft "$FILENAME"
            done
        else
            echo "$(date): No .obj files found. Waiting..."
        fi
    fi
done
