# Building the 42 C Formatter Extension

This document provides detailed instructions for building and packaging the 42 C Formatter extension.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/) (v12.x or later)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- [VS Code](https://code.visualstudio.com/) (for testing)

## Project Setup

1. Create a new directory for your extension:

```bash
mkdir c-formatter-42-ext
cd c-formatter-42-ext
```

2. Create the following project structure:

```
c-formatter-42-ext/
├── extension.js      # Main extension code
├── package.json      # Extension manifest
└── README.md         # Documentation
```

3. Copy the provided `extension.js`, `package.json`, and `README.md` files into their respective locations.

## Installing Dependencies

Install the required dependencies:

```bash
npm install
```

This will create a `node_modules` directory with all the necessary dependencies.

## Building and Packaging

### Testing Locally

To test the extension locally before packaging:

1. Open the extension directory in VS Code:

```bash
code .
```

2. Press `F5` to start debugging mode. This will:
   - Launch a new VS Code window with your extension loaded
   - Allow you to test the extension
   - Show console logs in the debug console

### Packaging as a VSIX File

To create a VSIX file that can be installed in VS Code:

```bash
npm run package
```

This will create a `.vsix` file in your project directory, which you can share or install.

### Publishing to VS Code Marketplace

To publish your extension to the VS Code Marketplace:

1. Create a publisher account on the [VS Code Marketplace](https://marketplace.visualstudio.com/manage)

2. Update your `package.json` with your publisher ID:

```json
"publisher": "yourPublisherID",
```

3. Install the VS Code Extension Manager globally:

```bash
npm install -g @vscode/vsce
```

4. Log in with your publisher account:

```bash
vsce login yourPublisherID
```

5. Publish your extension:

```bash
vsce publish
```

## Continuous Integration

You can set up GitHub Actions to automatically build and release your extension:

1. Create a `.github/workflows` directory in your project

2. Add a `build.yml` file with the following content:

```yaml
name: Build and Package

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    - name: Install dependencies
      run: npm install
    - name: Package Extension
      run: npm run package
    - name: Upload Artifact
      uses: actions/upload-artifact@v2
      with:
        name: extension
        path: "*.vsix"
```

This workflow will build and package your extension whenever changes are pushed to the main branch.

## Troubleshooting

### Common Issues

- **Missing Dependencies**: Make sure all dependencies are installed with `npm install`
- **VSIX Creation Fails**: Check that your `package.json` is correctly formatted
- **Extension Not Working**: Review console logs in the Debug Console when testing

### Getting Help

If you encounter issues, check:
- [VS Code Extension API Documentation](https://code.visualstudio.com/api)
- [VS Code Extension Development Guide](https://code.visualstudio.com/api/get-started/your-first-extension)