#!/bin/bash
# Installation script for c_formatter_42_wrapper
#
# This script installs the c_formatter_42_wrapper and (optionally) c_formatter_42
# in a way that works with IDE extensions and modern Python installations.

set -e

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${BLUE}Checking for Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}Error: Python not found. Please install Python 3.6 or higher.${NC}"
        exit 1
    else
        PYTHON="python"
    fi
else
    PYTHON="python3"
fi

PYTHON_VERSION=$($PYTHON --version | cut -d' ' -f2)
echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"

# Check if pip is installed
echo -e "${BLUE}Checking for pip installation...${NC}"
if ! $PYTHON -m pip --version &> /dev/null; then
    echo -e "${RED}Error: pip not found. Please install pip for Python.${NC}"
    exit 1
fi

# Check if pipx is installed and offer to use it
USE_PIPX=0
if command -v pipx &> /dev/null; then
    echo -e "${BLUE}pipx detected. Using pipx is recommended for isolated installations.${NC}"
    read -p "Would you like to use pipx for installation? [Y/n] " RESP
    if [[ "$RESP" != "n" && "$RESP" != "N" ]]; then
        USE_PIPX=1
    fi
else
    echo -e "${YELLOW}pipx not detected. Consider installing pipx for better package isolation.${NC}"
    echo -e "${YELLOW}You can install pipx with: $PYTHON -m pip install --user pipx${NC}"
    read -p "Would you like to install pipx now? [y/N] " RESP
    if [[ "$RESP" == "y" || "$RESP" == "Y" ]]; then
        echo -e "${BLUE}Installing pipx...${NC}"
        $PYTHON -m pip install --user pipx
        
        # Check if the installation was successful
        if command -v pipx &> /dev/null || $PYTHON -m pipx --version &> /dev/null; then
            echo -e "${GREEN}pipx installed successfully.${NC}"
            USE_PIPX=1
        else
            echo -e "${YELLOW}pipx installation detected issues. Falling back to pip.${NC}"
        fi
    fi
fi

# Install the wrapper
echo -e "${BLUE}Installing c_formatter_42_wrapper...${NC}"

# Current directory
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

if [[ $USE_PIPX -eq 1 ]]; then
    # Use pipx for installation
    if command -v pipx &> /dev/null; then
        PIPX_CMD="pipx"
    else
        PIPX_CMD="$PYTHON -m pipx"
    fi
    
    echo -e "${BLUE}Installing with pipx from $CURRENT_DIR...${NC}"
    $PIPX_CMD install "$CURRENT_DIR" --force
else
    # Use pip for installation
    echo -e "${BLUE}Installing with pip from $CURRENT_DIR...${NC}"
    $PYTHON -m pip install --user "$CURRENT_DIR"
fi

# Check if the wrapper was installed correctly
if command -v c_formatter_42_wrapper &> /dev/null || command -v c_formatter_42_wrapper.py &> /dev/null; then
    echo -e "${GREEN}c_formatter_42_wrapper installed successfully.${NC}"
else
    echo -e "${YELLOW}Warning: c_formatter_42_wrapper executable not found in PATH.${NC}"
    echo -e "${YELLOW}The package may have been installed but the executable is not in your PATH.${NC}"
fi

# Ask if the user wants to install c_formatter_42 as well
echo
read -p "Would you like to install c_formatter_42 as well? [Y/n] " RESP
if [[ "$RESP" != "n" && "$RESP" != "N" ]]; then
    echo -e "${BLUE}Installing c_formatter_42...${NC}"
    
    if [[ $USE_PIPX -eq 1 ]]; then
        echo -e "${BLUE}Installing with pipx...${NC}"
        $PIPX_CMD install c_formatter_42 --force
    else
        echo -e "${BLUE}Installing with pip...${NC}"
        $PYTHON -m pip install --user c_formatter_42
    fi
    
    # Check if c_formatter_42 was installed correctly
    if $PYTHON -c "import c_formatter_42" &> /dev/null; then
        echo -e "${GREEN}c_formatter_42 installed successfully.${NC}"
    else
        echo -e "${RED}Failed to import c_formatter_42. Installation may have issues.${NC}"
    fi
fi

# Configure VS Code/Cursor if installed
echo
read -p "Would you like to configure VS Code/Cursor to use the wrapper? [Y/n] " RESP
if [[ "$RESP" != "n" && "$RESP" != "N" ]]; then
    VS_CODE_SETTINGS=""
    
    # Check for VS Code settings
    for settings_path in \
        "$HOME/Library/Application Support/Code/User/settings.json" \
        "$HOME/.config/Code/User/settings.json" \
        "$HOME/AppData/Roaming/Code/User/settings.json" \
        "$HOME/Library/Application Support/Cursor/User/settings.json" \
        "$HOME/.config/Cursor/User/settings.json" \
        "$HOME/AppData/Roaming/Cursor/User/settings.json"
    do
        if [[ -f "$settings_path" ]]; then
            VS_CODE_SETTINGS="$settings_path"
            echo -e "${GREEN}Found settings at: $VS_CODE_SETTINGS${NC}"
            break
        fi
    done
    
    if [[ -z "$VS_CODE_SETTINGS" ]]; then
        echo -e "${YELLOW}Could not find VS Code or Cursor settings.json.${NC}"
        echo -e "${YELLOW}Please manually configure the formatter in your editor settings:${NC}"
        echo -e "${YELLOW}  \"c-formatter-42.formatCommand\": \"c_formatter_42_wrapper\"${NC}"
    else
        echo -e "${BLUE}Updating settings to use the wrapper...${NC}"
        
        # Check if jq is installed
        if command -v jq &> /dev/null; then
            # Create a backup
            cp "$VS_CODE_SETTINGS" "${VS_CODE_SETTINGS}.bak"
            
            # Update the settings using jq
            jq '. + {"c-formatter-42.formatCommand": "c_formatter_42_wrapper"}' "$VS_CODE_SETTINGS" > "${VS_CODE_SETTINGS}.tmp"
            mv "${VS_CODE_SETTINGS}.tmp" "$VS_CODE_SETTINGS"
            
            echo -e "${GREEN}Settings updated successfully. Backup saved to ${VS_CODE_SETTINGS}.bak${NC}"
        else
            echo -e "${YELLOW}jq tool not found. Cannot automatically update settings.${NC}"
            echo -e "${YELLOW}Please manually add the following to your settings.json:${NC}"
            echo -e "${YELLOW}  \"c-formatter-42.formatCommand\": \"c_formatter_42_wrapper\"${NC}"
        fi
    fi
fi

# Create a configuration file
CONFIG_DIR="$HOME/.config/c_formatter_42"
if [[ ! -d "$CONFIG_DIR" ]]; then
    mkdir -p "$CONFIG_DIR"
fi

CONFIG_FILE="$CONFIG_DIR/config"
echo -e "${BLUE}Creating configuration file at $CONFIG_FILE...${NC}"

cat > "$CONFIG_FILE" << EOF
# c_formatter_42_wrapper configuration

# Path to the c_formatter_42 executable or directory
# Uncomment and set this if you want to specify a custom path
# C_FORMATTER_42_PATH=/path/to/c_formatter_42

# Debug mode (set to 1 to enable debug logging)
# C_FORMATTER_42_WRAPPER_DEBUG=0
EOF

echo -e "${GREEN}Configuration file created at $CONFIG_FILE${NC}"

# Final instructions
echo
echo -e "${GREEN}Installation completed!${NC}"
echo
echo -e "${BLUE}To use the formatter from the command line:${NC}"
echo -e "  c_formatter_42_wrapper file.c"
echo
echo -e "${BLUE}To configure VS Code/Cursor manually:${NC}"
echo -e "  1. Open Settings (Ctrl+, or Cmd+, on macOS)"
echo -e "  2. Search for 'c-formatter-42'"
echo -e "  3. Set 'Format Command' to 'c_formatter_42_wrapper'"
echo
echo -e "${BLUE}If you have any issues:${NC}"
echo -e "  1. Enable debug mode in the extension settings"
echo -e "  2. Check the configuration file at $CONFIG_FILE"
echo -e "  3. Run with --wrapper-verbose flag for more information"
echo

exit 0
