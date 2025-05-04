# Installation Guide for c_formatter_42 Wrapper

This guide will help you install and configure the c_formatter_42 wrapper to solve Python environment compatibility issues with IDE extensions.

## Overview

The c_formatter_42_wrapper is a solution to the Python environment compatibility issues that occur when using c_formatter_42 with IDE extensions like VSCode or Cursor. It provides a robust way to find and use c_formatter_42 regardless of where it's installed, making it work seamlessly across different Python environments.

## Installation Methods

There are several ways to install the wrapper, depending on your preferences and requirements:

### Method 1: Using the Automated Installation Script (Recommended)

The easiest way to install the wrapper is to use the provided installation script:

1. Navigate to the wrapper directory
   ```bash
   cd /Users/marta/Documents/PROJECTS/c-formatter-42-ext/wrapper
   ```

2. Make the script executable
   ```bash
   chmod +x install.sh
   ```

3. Run the installation script
   ```bash
   ./install.sh
   ```

4. Follow the prompts to complete the installation

The script will:
- Check your Python installation
- Offer to use pipx for better isolation (recommended)
- Install the wrapper
- Optionally install c_formatter_42
- Optionally configure VSCode/Cursor to use the wrapper

### Method 2: Installing with pip

If you prefer to install manually with pip:

```bash
# Navigate to the wrapper directory
cd /Users/marta/Documents/PROJECTS/c-formatter-42-ext/wrapper

# Install for the current user
pip install --user .

# Or install system-wide (not recommended due to PEP 668)
pip install .
```

### Method 3: Installing with pipx (Recommended)

pipx provides better isolation and avoids conflicts with other Python packages:

```bash
# Install pipx if you don't have it
pip install --user pipx

# Install the wrapper
pipx install /Users/marta/Documents/PROJECTS/c-formatter-42-ext/wrapper
```

## Configuring Your IDE

### VSCode / Cursor Configuration

1. Open Settings (Ctrl+, or Cmd+, on macOS)
2. Search for "c-formatter-42"
3. Set "Format Command" to `c_formatter_42_wrapper`
4. Optionally enable "Debug" for more detailed logging

Alternatively, add the following to your `settings.json`:

```json
{
  "c-formatter-42.formatCommand": "c_formatter_42_wrapper",
  "c-formatter-42.debug": false
}
```

## Environment Variables

The wrapper supports the following environment variables:

- `C_FORMATTER_42_PATH`: Path to the c_formatter_42 executable or directory
  ```bash
  # Example: Set to a custom installation
  export C_FORMATTER_42_PATH=/path/to/c_formatter_42
  ```

- `C_FORMATTER_42_WRAPPER_DEBUG`: Enable debug logging
  ```bash
  # Enable debug logging
  export C_FORMATTER_42_WRAPPER_DEBUG=1
  ```

## Configuration File

The wrapper also supports a configuration file at `~/.config/c_formatter_42/config`. This file is created by the installation script, but you can edit it manually:

```
# c_formatter_42_wrapper configuration

# Path to the c_formatter_42 executable or directory
# Uncomment and set this if you want to specify a custom path
# C_FORMATTER_42_PATH=/path/to/c_formatter_42

# Debug mode (set to 1 to enable debug logging)
# C_FORMATTER_42_WRAPPER_DEBUG=0
```

## Verifying the Installation

To verify that the wrapper is working correctly:

```bash
# Check if the wrapper is in your PATH
which c_formatter_42_wrapper

# Test the wrapper with the --wrapper-path flag
c_formatter_42_wrapper --wrapper-path

# Format a test file
c_formatter_42_wrapper /path/to/test.c
```

## Troubleshooting

If you encounter issues with the wrapper:

1. **Wrapper Not Found**: Make sure it's installed and in your PATH
   ```bash
   # Check the installation
   which c_formatter_42_wrapper
   ```

2. **Python Environment Issues**: Check if the wrapper can find c_formatter_42
   ```bash
   # Enable debug logging
   export C_FORMATTER_42_WRAPPER_DEBUG=1
   c_formatter_42_wrapper --wrapper-path
   ```

3. **IDE Extension Issues**: Enable debug logging in the extension settings and check the editor's output console

4. **macOS Permissions**: On macOS, you might need to grant permission to execute the wrapper
   ```bash
   chmod +x $(which c_formatter_42_wrapper)
   ```

## Uninstalling

To uninstall the wrapper:

```bash
# If installed with pip
pip uninstall c_formatter_42_wrapper

# If installed with pipx
pipx uninstall c_formatter_42_wrapper
```

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
