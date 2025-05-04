#!/bin/bash
# c_formatter_42_wrapper.sh
# 
# A simple shell wrapper that finds the Python interpreter
# and runs the Python wrapper script

# Determine the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
WRAPPER_PY="$SCRIPT_DIR/c_formatter_42_wrapper.py"

# Check if the Python wrapper exists
if [ ! -f "$WRAPPER_PY" ]; then
    echo "Error: Could not find the Python wrapper script at $WRAPPER_PY" >&2
    exit 1
fi

# Find Python interpreter
PYTHON=$(command -v python3)
if [ -z "$PYTHON" ]; then
    PYTHON=$(command -v python)
    if [ -z "$PYTHON" ]; then
        echo "Error: Could not find Python interpreter" >&2
        exit 1
    fi
fi

# Make sure the Python wrapper is executable
chmod +x "$WRAPPER_PY" 2>/dev/null

# Check if we're being called with a special flag to print the version
if [ "$1" = "--wrapper-version" ]; then
    echo "c_formatter_42_wrapper v0.1.0"
    exit 0
fi

# Run the Python wrapper with all arguments
"$PYTHON" "$WRAPPER_PY" "$@"
exit $?
