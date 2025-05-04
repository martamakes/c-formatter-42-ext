# c_formatter_42_wrapper

A wrapper for [c_formatter_42](https://github.com/cacharle/c_formatter_42) that resolves Python environment compatibility issues and adds full norminette compliance.

## Features

- **Full Norminette Compliance**: 
  - Properly formats 42 headers with correct alignment
  - Fixes space/tab issues
  - Properly separates variable declarations and initializations
  - Ensures newlines after variable declarations
  - Fixes braces and newlines
  - Prevents empty lines in functions
  - Ensures newline at end of file

- **Python Environment Compatibility**:
  - Multiple detection methods for finding the correct c_formatter_42 installation
  - Environment variable configuration (`C_FORMATTER_42_PATH`)
  - Support for pipx, virtualenv, and system installations
  - Fall back mechanisms for ensuring the formatter is always found
  - Compatible with IDE extensions (VSCode, Cursor, etc.)

## Installation

You can install the wrapper using several methods:

### Using pip

```bash
pip install c_formatter_42_wrapper
```

### Using pipx (recommended)

```bash
pipx install c_formatter_42_wrapper
```

This installs the wrapper in an isolated environment while still making it available in your PATH.

### From source

```bash
git clone https://github.com/martamakes/c-formatter-42-ext.git
cd c-formatter-42-ext/wrapper
pip install .
```

### Using the install script

The wrapper includes an installation script that will guide you through the process:

```bash
cd c-formatter-42-ext/wrapper
chmod +x install.sh
./install.sh
```

## Usage

The wrapper can be used in two modes:

### Basic Mode (Compatible with original c_formatter_42)

```bash
c_formatter_42_wrapper file.c
```

This behaves exactly like the original c_formatter_42 formatter.

### Enhanced Mode (Full Norminette Compliance)

```bash
c_formatter_42_wrapper --enhanced file.c
```

The enhanced mode adds full norminette compliance, including proper 42 header formatting.

You can specify your 42 intra handle and email for the header:

```bash
c_formatter_42_wrapper --enhanced --username "mvigara-" --email "mvigara-@student.42madrid.com" file.c
```

### Environment Variables

- `C_FORMATTER_42_PATH`: Path to the c_formatter_42 executable or directory
- `C_FORMATTER_42_WRAPPER_DEBUG`: Set to "1", "true", or "yes" to enable debug logging
- `NORMINETTE_FORMATTER_DEBUG`: Set to "1", "true", or "yes" to enable debug logging for the enhanced formatter

### Wrapper-specific flags

- `--wrapper-verbose`: Enable debug logging
- `--wrapper-path`: Print the path to the formatter and exit
- `--enhanced`: Use enhanced formatting mode for full norminette compliance
- `--username`: Specify your 42 intra handle for header
- `--email`: Specify your 42 email for header

## IDE Integration

To use the wrapper in IDE extensions:

1. Install the extension as usual
2. Configure the extension to use `c_formatter_42_wrapper` instead of `c_formatter_42`
3. Enable enhanced mode and set your 42 intra handle and email in the settings

### VSCode / Cursor

In your settings.json:

```json
{
  "c-formatter-42.formatCommand": "c_formatter_42_wrapper",
  "c-formatter-42.enhancedMode": true,
  "c-formatter-42.username": "mvigara-",
  "c-formatter-42.email": "mvigara-@student.42madrid.com"
}
```

You can also use the "Set 42 Intra Handle and Email" command from the command palette to configure these settings.

## How it Works

The wrapper uses a series of detection methods to find the c_formatter_42 installation:

1. Check the `C_FORMATTER_42_PATH` environment variable
2. Look for the executable in PATH
3. Try to import the Python module
4. Check common installation locations (pipx, user site-packages, virtualenv)
5. Check Homebrew cellar (on macOS)
6. Fall back to the `which` command

In enhanced mode, it also applies additional formatting rules to ensure full norminette compliance.

## Requirements

- Python 3.6 or higher
- c_formatter_42 installed somewhere on the system

## License

MIT
