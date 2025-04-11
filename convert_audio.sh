#!/bin/bash

# Convert WAV audio files to MP3 for better web browser compatibility
# Usage: ./convert_audio.sh [directory]

# Set default directory to current directory if not specified
DIR=${1:-.}

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install it first."
    echo "On Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "On CentOS/RHEL: sudo yum install ffmpeg"
    echo "On macOS with Homebrew: brew install ffmpeg"
    exit 1
fi

# Count WAV files in directory
WAV_COUNT=$(find "$DIR" -name "*.wav" | wc -l)

if [ "$WAV_COUNT" -eq 0 ]; then
    echo "No WAV files found in $DIR"
    exit 0
fi

echo "Found $WAV_COUNT WAV file(s) to convert"

# Convert each WAV file to MP3
find "$DIR" -name "*.wav" | while read -r wavfile; do
    mp3file="${wavfile%.wav}.mp3"
    
    # Check if MP3 already exists
    if [ -f "$mp3file" ]; then
        echo "Skipping $wavfile (MP3 already exists)"
        continue
    fi
    
    echo "Converting $wavfile to MP3..."
    ffmpeg -i "$wavfile" -codec:a libmp3lame -qscale:a 2 "$mp3file" -loglevel error
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully converted to $mp3file"
    else
        echo "✗ Failed to convert $wavfile"
    fi
done

echo "Conversion complete!"
echo "Remember to update your HTML audio tags to include both formats:"
echo "<audio controls>"
echo '  <source src="path/to/file.wav" type="audio/wav">'
echo '  <source src="path/to/file.mp3" type="audio/mpeg">'
echo "  Your browser does not support the audio element."
echo "</audio>"
