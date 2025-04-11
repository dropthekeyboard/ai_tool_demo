#!/bin/bash

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install it first."
    echo "Run: sudo apt install ffmpeg"
    exit 1
fi

# Check if input file is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 input.mp4 [output.gif] [speed] [sensitivity] [--noskip]"
    echo "  - output.gif: Optional output filename"
    echo "  - speed: Optional speed multiplier (default: 4, higher = faster)"
    echo "  - sensitivity: Optional value 1-10 (default: 5, higher = skip more frames)"
    echo "  - --noskip: Optional flag to disable frame skipping"
    exit 1
fi

INPUT_FILE="$1"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' does not exist"
    exit 1
fi

# Parse arguments
OUTPUT_FILE=""
SPEED=4
SENSITIVITY=5
SKIP_FRAMES=true

# Parse remaining arguments
for arg in "${@:2}"; do
    if [[ "$arg" == *.gif ]]; then
        OUTPUT_FILE="$arg"
    elif [[ "$arg" =~ ^[0-9]+(\.[0-9]+)?$ ]] && (( $(echo "$arg < 100" | bc -l) )); then
        SPEED="$arg"
    elif [[ "$arg" =~ ^[0-9]+$ ]] && [ "$arg" -ge 1 ] && [ "$arg" -le 10 ]; then
        SENSITIVITY="$arg"
    elif [[ "$arg" == "--noskip" ]]; then
        SKIP_FRAMES=false
    fi
done

# If output file wasn't specified, create a default name
if [ -z "$OUTPUT_FILE" ]; then
    if [ "$SKIP_FRAMES" = true ]; then
        OUTPUT_FILE="${INPUT_FILE%.*}_${SPEED}x.gif"
    else
        OUTPUT_FILE="${INPUT_FILE%.*}_${SPEED}x_noskip.gif"
    fi
fi

# Calculate setpts value (inverse of speed)
SETPTS=$(awk "BEGIN {print 1/$SPEED}")

# Define filters based on whether frame skipping is enabled
if [ "$SKIP_FRAMES" = true ]; then
    # Calculate mpdecimate values based on sensitivity
    HI=$((64 * 12 * (11 - SENSITIVITY) / 5))
    LO=$((64 * 5 * (11 - SENSITIVITY) / 5))
    FRAC=$(awk "BEGIN {print 0.33 + ($SENSITIVITY * 0.05)}")
    
    echo "Converting $INPUT_FILE to GIF with ${SPEED}x speed-up..."
    echo "Frame skip sensitivity: $SENSITIVITY (hi=$HI, lo=$LO, frac=$FRAC)"
    
    FILTER_CHAIN="mpdecimate=hi=$HI:lo=$LO:frac=$FRAC,setpts=N/FRAME_RATE/TB,setpts=${SETPTS}*PTS,fps=15,scale=640:-1:flags=lanczos"
else
    echo "Converting $INPUT_FILE to GIF with ${SPEED}x speed-up (no frame skipping)..."
    
    FILTER_CHAIN="setpts=${SETPTS}*PTS,fps=15,scale=640:-1:flags=lanczos"
fi

# Convert MP4 to GIF with custom speed up and frame skipping
ffmpeg -i "$INPUT_FILE" -vf "$FILTER_CHAIN" -loop 0 "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Conversion completed successfully! Output: $OUTPUT_FILE"
    echo "Original size: $(du -h "$INPUT_FILE" | cut -f1)"
    echo "GIF size: $(du -h "$OUTPUT_FILE" | cut -f1)"
else
    echo "Error: Conversion failed"
    exit 1
fi