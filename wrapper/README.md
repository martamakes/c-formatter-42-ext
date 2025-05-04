# c_formatter_42_wrapper

A wrapper for [c_formatter_42](https://github.com/cacharle/c_formatter_42) that resolves Python environment compatibility issues, particularly when used in IDE extensions.

## Features

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

## Usage

The wrapper can be used exactly like the original c_formatter_42:

```bash
c_formatter_42_wrapper file.c
```

It accepts all the same options as c_formatter_42.

### Environment Variables

- `C_FORMATTER_42_PATH`: Path to the c_formatter_42 executable or directory
- `C_FORMATTER_42_WRAPPER_DEBUG`: Set to "1", "true", or "yes" to enable debug logging

### Wrapper-specific flags

- `--wrapper-verbose`: Enable debug logging
- `--wrapper-path`: Print the path to the formatter and exit
- `--wrapper-version`: Print the wrapper version and exit

## IDE Integration

To use the wrapper in IDE extensions:

1. Install the extension as usual
2. Configure the extension to use `c_formatter_42_wrapper` instead of `c_formatter_42`

### VSCode / Cursor

In your settings.json:

```json
{
  "c-formatter-42.formatCommand": "c_formatter_42_wrapper"
}
```

## How it Works

The wrapper uses a series of detection methods to find the c_formatter_42 installation:

1. Check the `C_FORMATTER_42_PATH` environment variable
2. Look for the executable in PATH
3. Try to import the Python module
4. Check common installation locations (pipx, user site-packages, virtualenv)
5. Check Homebrew cellar (on macOS)
6. Fall back to the `which` command

If the executable is found, it's called directly. If only the module is found, the wrapper creates a temporary script that imports and runs the module.

## Requirements

- Python 3.6 or higher
- c_formatter_42 installed somewhere on the system

## License

MIT
