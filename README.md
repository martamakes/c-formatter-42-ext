# 42 C Formatter VSCode/Cursor Extension

A VS Code extension that integrates with the c_formatter_42 tool to automatically format C code according to the 42 School norminette standards. Just learning for fun how to create VSCode or any VSCode fork IDE extension.

Created by mvigara- (Marta)

## Description

This extension provides seamless integration of the c_formatter_42 Python package into Visual Studio Code and Cursor. It enables you to automatically format your C code to comply with the 42 School's strict formatting guidelines with a single command or on file save.

## Why Use This Extension Instead of Just c_formatter_42?

This extension enhances your development workflow in several ways that aren't possible with the standalone c_formatter_42 tool:

1. **Integrated Experience** - Format your code directly within your editor without switching to the terminal
2. **Format on Save** - Automatically apply formatting every time you save a file
3. **Editor Commands** - Access formatting through the command palette or keyboard shortcuts
4. **Visual Feedback** - Get notifications about formatting status and errors
5. **Smoother Workflow** - Eliminate the need to manually specify files to format
6. **Team Consistency** - Ensure everyone on your team uses the same formatter with the same settings
7. **Automatic Installation** - Option to automatically install the formatter if not found

Simply put, this extension turns the c_formatter_42 tool from a manual, command-line utility into a seamless part of your coding workflow, saving you time and ensuring consistent code quality with minimal effort.

## Documentation

- [Building Instructions](./BUILDING.md) - Detailed guide for building and packaging the extension
- [Customization Guide](./CUSTOMIZING.md) - How to modify this extension for other formatters
- [VSCode Extension Guide](./VSCODE_EXTENSION_GUIDE.md) - Comprehensive guide on creating VSCode extensions

## Features

- Format C files according to 42 School norminette standards
- Format on save capability (optional)
- Auto-detection of the c_formatter_42 tool
- Option to install the formatter if not found
- Works in both VSCode and Cursor editors
- Custom formatting command

## Requirements

- Visual Studio Code or Cursor
- Python 3.x
- c_formatter_42 Python package (`pip install c_formatter_42`)

## Installation

### Installing c_formatter_42

```bash
# Install globally
pip install c_formatter_42

# OR install for current user only
pip install --user c_formatter_42
```

### Installing the Extension

1. Download the `.vsix` file from the releases page
2. In VSCode/Cursor, go to Extensions view (Ctrl+Shift+X or Cmd+Shift+X on macOS)
3. Click on "..." menu in the Extensions sidebar and select "Install from VSIX..."
4. Navigate to the downloaded `.vsix` file and select it

## Usage

Once installed, the extension will provide formatting capabilities for C files:

1. Open a C file (with `.c` or `.h` extension)
2. To format the current file, you can:
   - Right-click and select "Format Document"
   - Use the keyboard shortcut `Shift+Alt+F` (or `Shift+Option+F` on macOS)
   - Press `F1` to open the command palette, then type "Format Document" and press Enter
   - Use the custom command "Format with 42 C Formatter" from the command palette

## Extension Settings

- `c-formatter-42.enableFormatOnSave`: Enable automatic formatting when saving C files
- `c-formatter-42.formatCommand`: The command to execute c_formatter_42 (default: "c_formatter_42")
- `c-formatter-42.installOnStartup`: Automatically attempt to install c_formatter_42 if not found on startup

## Building from Source

1. Clone the repository
2. Install dependencies: `npm install`
3. Package the extension: `npm run package`

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to help improve this extension.

## License

MIT

## Acknowledgments

- [c_formatter_42](https://github.com/cacharle/c_formatter_42) by Charles Cabergs (cacharle)
- All the students at 42 School