# 42 C Formatter VSCode/Cursor Extension

A VS Code extension that integrates with the c_formatter_42 tool to automatically format C code according to the 42 School norminette standards. Just learning for fun how to create VSCode or any VSCode fork IDE extension.

Created by mvigara- (@martamakes)

## Description

This extension provides seamless integration of the c_formatter_42 Python package into Visual Studio Code and Cursor. It enables you to automatically format your C code to comply with the 42 School's strict formatting guidelines with a single command or on file save.

## New in Version 0.2.1: Enhanced Formatter with Full Norminette Compliance

The latest version includes an enhanced formatter mode that addresses all norminette requirements:

- **42 Header Integration** - Automatically adds the properly aligned 42 header if missing
- **Spaces vs Tabs Correction** - Fixes the SPACE_REPLACE_TAB error
- **Variable Declaration Separation** - Separates declaration and initialization to fix DECL_ASSIGN_LINE errors
- **Proper Newlines** - Adds newlines after variable declarations (NL_AFTER_VAR_DECL) and braces (BRACE_SHOULD_EOL)
- **End-of-File Newline** - Ensures files end with a newline

## New Feature: Custom 42 Information

You can now set your 42 intra handle and email for the header:

- Use the "Set 42 Intra Handle and Email" command from the command palette
- Or configure in settings: `c-formatter-42.username` and `c-formatter-42.email`

## New in Version 0.2.0: Python Environment Compatibility Improvements

The previous version includes major improvements to resolve Python environment compatibility issues:

- **Environment-Independent Formatter Wrapper** - Automatically finds and uses c_formatter_42 regardless of where it's installed 
- **Multiple Installation Detection Methods** - Works with pipx, virtualenv, system-wide, and homebrew installations
- **Environment Variable Configuration** - Supports `C_FORMATTER_42_PATH` for custom installations
- **Robust Fallback Mechanism** - Ensures formatting works even with complex Python configurations
- **Improved IDE Compatibility** - Better support for VSCode, Cursor and other editors

## Why Use This Extension Instead of Just c_formatter_42?

This extension enhances your development workflow in several ways that aren't possible with the standalone c_formatter_42 tool:

1. **Integrated Experience** - Format your code directly within your editor without switching to the terminal
2. **Format on Save** - Automatically apply formatting every time you save a file
3. **Editor Commands** - Access formatting through the command palette or keyboard shortcuts
4. **Visual Feedback** - Get notifications about formatting status and errors
5. **Smoother Workflow** - Eliminate the need to manually specify files to format
6. **Team Consistency** - Ensure everyone on your team uses the same formatter with the same settings
7. **Automatic Installation** - Option to automatically install the formatter if not found
8. **Environment Compatibility** - Works with any Python setup thanks to the wrapper
9. **Full Norminette Compliance** - Fixes all common norminette errors, not just basic formatting

Simply put, this extension turns the c_formatter_42 tool from a manual, command-line utility into a seamless part of your coding workflow, saving you time and ensuring consistent code quality with minimal effort.

## Documentation

- [Building Instructions](./BUILDING.md) - Detailed guide for building and packaging the extension
- [Customization Guide](./CUSTOMIZING.md) - How to modify this extension for other formatters
- [VSCode Extension Guide](./CREATE_YOUR_OWN_EXTENSION_MICROGUIDE.md) - Comprehensive guide on creating VSCode extensions
- [Installation Guide](./INSTALLATION.md) - Detailed installation instructions
- [Solution Details](./SOLUTION.md) - Technical information about the solution

## Features

- Format C files according to 42 School norminette standards
- Format on save capability (optional)
- Auto-detection of the c_formatter_42 tool across different Python environments
- Enhanced formatter mode for full norminette compliance
- Proper 42 header support with your intra handle and email
- Multiple installation methods supported (pip, pipx, homebrew)
- Environment variable configuration (`C_FORMATTER_42_PATH`)
- Option to install the formatter if not found
- Works in both VSCode and Cursor editors
- Custom formatting command

## Requirements

- Visual Studio Code or Cursor
- Python 3.x
- c_formatter_42 Python package

## Installation

### Installing c_formatter_42 and the Wrapper

You have several options for installing the formatter:

```bash
# Option 1: Install the wrapper (recommended)
pip install c_formatter_42_wrapper

# Option 2: Install both the wrapper and the formatter
pip install c_formatter_42_wrapper c_formatter_42

# Option 3: Install using pipx for isolation (best practice)
pipx install c_formatter_42_wrapper
```

### Installing the Extension

1. Download the `.vsix` file from the releases page
2. In VSCode/Cursor, go to Extensions view (Ctrl+Shift+X or Cmd+Shift+X on macOS)
3. Click on "..." menu in the Extensions sidebar and select "Install from VSIX..."
4. Navigate to the downloaded `.vsix` file and select it

```bash
code --install-extension c-formatter-42-0.2.1.vsix
```

## Usage

Once installed, the extension will provide formatting capabilities for C files:

1. Open a C file (with `.c` or `.h` extension)
2. Use "Set 42 Intra Handle and Email" command from the command palette to set your 42 information
3. To format the current file, you can:
   - Right-click and select "Format Document"
   - Use the keyboard shortcut `Shift+Alt+F` (or `Shift+Option+F` on macOS)
   - Press `F1` to open the command palette, then type "Format Document" and press Enter
   - Use the custom command "Format with 42 C Formatter" from the command palette

## Extension Settings

- `c-formatter-42.enableFormatOnSave`: Enable automatic formatting when saving C files
- `c-formatter-42.formatCommand`: The command to execute for formatting (default: `c_formatter_42_wrapper`)
- `c-formatter-42.executablePath`: Full path to the formatter executable (optional)
- `c-formatter-42.installOnStartup`: Automatically attempt to install the wrapper if not found
- `c-formatter-42.enhancedMode`: Use enhanced formatter mode for full norminette compliance (default: true)
- `c-formatter-42.debug`: Enable debug logging for the wrapper
- `c-formatter-42.username`: Your 42 intra handle for the header (e.g., "mvigara-")
- `c-formatter-42.email`: Your 42 email for the header (e.g., "mvigara-@student.42madrid.com")
- `c-formatter-42.environmentVariables`: Custom environment variables to set when running the formatter

## Environment Variables

The wrapper supports the following environment variables:

- `C_FORMATTER_42_PATH`: Path to the c_formatter_42 executable or directory
- `C_FORMATTER_42_WRAPPER_DEBUG`: Set to "1", "true", or "yes" to enable debug logging
- `NORMINETTE_FORMATTER_DEBUG`: Set to "1", "true", or "yes" to enable debug logging for the enhanced formatter

## Enhanced Formatter Mode

The enhanced formatter mode adds functionality to make your code fully compliant with norminette requirements:

1. **42 Header**: Automatically adds a properly aligned 42 header if missing
   - Uses your intra handle and email from settings
   - Automatically pads all fields to align correctly

2. **Variable Declaration**: Separates declaration and initialization
   ```c
   // Before formatting:
   int i = 0;
   
   // After formatting:
   int i;
   
   i = 0;
   ```

3. **Spacing and Indentation**: Ensures proper use of tabs instead of spaces for indentation

4. **Braces and Newlines**: Ensures proper newlines after braces and variable declarations

5. **Newline at EOF**: Makes sure all files end with a newline

## Troubleshooting

If you're experiencing issues with the formatter:

1. **Formatter Not Found**: Make sure you have either `c_formatter_42_wrapper` or `c_formatter_42` installed
   - Check with `which c_formatter_42_wrapper` or `pip list | grep c-formatter-42`

2. **Python Environment Issues**: If the extension can't find the formatter, try these solutions:
   - Install the wrapper: `pip install c_formatter_42_wrapper`
   - Set the `C_FORMATTER_42_PATH` environment variable to the location of your formatter
   - Specify the full path in the `c-formatter-42.executablePath` setting

3. **Header Issues**: If the 42 header is incorrect:
   - Use the "Set 42 Intra Handle and Email" command to configure your info
   - Check that the settings `c-formatter-42.username` and `c-formatter-42.email` are set correctly

4. **Debug Mode**: Enable debug logging in the extension settings to get more information

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
- [42 Header VSCode Extension](https://github.com/kube/vscode-42header) by Kube
- All the students at 42 School
