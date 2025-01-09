#!/bin/bash

if [ $# -eq 1 ]; then
    input_file="$1"
    echo "Writing..."
    python EEPROM-fwd.py $input_file
    echo "Diff:"
    xxd "$input_file" | diff - <(python EEPROM-fr.py -- | xxd)
elif [ $# -eq 2 ]; then
    input_file="$1"
    output_file="$2"
    echo "Writing..."
    python EEPROM-fwd.py $input_file
    echo "Reading..."
    python EEPROM-fr.py $output_file
    echo "Diff:"
    xxd "$input_file" | diff - <(xxd "$output_file")

else
    echo "Invalid number of arguments. Please provide 1 or 2 file paths."
fi
