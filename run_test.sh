#!/bin/bash
# Test script for the enhanced formatter

# Set debug mode
export C_FORMATTER_42_WRAPPER_DEBUG=1
export NORMINETTE_FORMATTER_DEBUG=1

# Make sure our scripts are executable
chmod +x wrapper/c_formatter_42_wrapper.py
chmod +x wrapper/norminette_formatter.py

# Run the enhanced formatter on the test file
echo "Running enhanced formatter on test_enhanced.c..."
wrapper/c_formatter_42_wrapper.py --enhanced --wrapper-verbose test_enhanced.c

# Display the formatted file
echo "Formatted file content:"
cat test_enhanced.c

# Run norminette on the formatted file to check compliance
if command -v norminette &> /dev/null; then
    echo "Running norminette check..."
    norminette test_enhanced.c
else
    echo "Norminette not found. Skipping compliance check."
fi

echo "Formatting complete!"
