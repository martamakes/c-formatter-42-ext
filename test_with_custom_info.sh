#!/bin/bash
# Test script for the enhanced formatter with custom 42 info

# This script tests the formatter with custom 42 intra handle and email

# Set debug mode
export C_FORMATTER_42_WRAPPER_DEBUG=1
export NORMINETTE_FORMATTER_DEBUG=1

# Make sure our scripts are executable
chmod +x wrapper/c_formatter_42_wrapper.py
chmod +x wrapper/norminette_formatter.py

# Sample 42 info (replace with your actual info)
USERNAME="mvigara-"
EMAIL="mvigara-@student.42madrid.com"

# Copy the test file to a new file for testing
cp test.c test_with_custom_info.c

# Run the enhanced formatter on the test file with custom info
echo "Running enhanced formatter on test_with_custom_info.c with custom 42 info..."
wrapper/c_formatter_42_wrapper.py --enhanced --wrapper-verbose --username "$USERNAME" --email "$EMAIL" test_with_custom_info.c

# Display the formatted file content
echo "Formatted file content:"
cat test_with_custom_info.c

# Run norminette on the formatted file to check compliance
if command -v norminette &> /dev/null; then
    echo "Running norminette check..."
    norminette test_with_custom_info.c
else
    echo "Norminette not found. Skipping compliance check."
fi

echo "Formatting complete!"
