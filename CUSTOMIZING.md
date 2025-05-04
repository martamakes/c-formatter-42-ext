# Customizing the 42 C Formatter Extension

This guide explains how to customize the extension.js file to create your own VS Code extension for any custom formatter.

## Understanding the Extension Structure

The extension consists of two main files:
- `package.json`: Defines metadata, dependencies, and activation events
- `extension.js`: Contains the actual extension code

## Customizing the Extension

### 1. Modifying package.json

To adapt this extension for a different formatter:

#### Basic Information
```json
{
  "name": "your-formatter-name",
  "displayName": "Your Formatter Display Name",
  "description": "Your formatter description",
  "version": "0.1.0",
  "publisher": "yourPublisherID",
  // Other fields...
}
```

#### Language Support
Change the activation event to target different languages:
```json
"activationEvents": [
  "onLanguage:python"  // Change "c" to your target language
]
```

#### Commands and Configuration
```json
"contributes": {
  "commands": [
    {
      "command": "your-formatter.format",
      "title": "Format with Your Formatter"
    }
  ],
  "configuration": {
    "title": "Your Formatter",
    "properties": {
      "your-formatter.enableFormatOnSave": {
        "type": "boolean",
        "default": false,
        "description": "Enable formatting on save"
      },
      "your-formatter.formatCommand": {
        "type": "string",
        "default": "your-formatter-command",
        "description": "Command to execute your formatter"
      }
      // Add more configuration options as needed
    }
  }
}
```

### 2. Customizing extension.js

#### Change the Formatter Provider
Adjust the language ID check:
```javascript
provideDocumentFormattingEdits(document) {
    if (document.languageId !== 'python') { // Change 'c' to your target language
        return [];
    }
    
    return formatDocument(document);
}
```

#### Update Command Registration
```javascript
context.subscriptions.push(
    vscode.commands.registerCommand('your-formatter.format', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'python') { // Change 'c' to your target language
            vscode.window.showErrorMessage('This command only works with Python files'); // Update message
            return;
        }

        vscode.commands.executeCommand('editor.action.formatDocument');
    })
);
```

#### Modify the Formatting Logic
The most important part to customize is the `formatDocument` function:

```javascript
async function formatDocument(document) {
    return new Promise((resolve, reject) => {
        // Get the configuration
        const config = vscode.workspace.getConfiguration('your-formatter');
        const formatCommand = config.get('formatCommand', 'your-formatter-command');

        // Check if your formatter is available
        try {
            which.sync(formatCommand.split(' ')[0]);
        } catch (err) {
            vscode.window.showErrorMessage(
                `Your Formatter: ${formatCommand} not found. Please install it with 'pip install your-formatter'`
            );
            return resolve([]);
        }

        // Create a temporary file for passing content to your formatter
        const tmpDir = os.tmpdir();
        const tmpFilePath = path.join(tmpDir, `vscode_format_${Date.now()}.py`); // Change extension as needed

        try {
            // Write current content to temporary file
            fs.writeFileSync(tmpFilePath, document.getText());

            // Execute your formatter on the temporary file
            // Modify command line arguments as needed for your formatter
            exec(`${formatCommand} "${tmpFilePath}"`, (error, stdout, stderr) => {
                try {
                    if (error) {
                        vscode.window.showErrorMessage(`Your Formatter error: ${stderr || error.message}`);
                        return resolve([]);
                    }

                    // Read formatted content
                    const formattedText = fs.readFileSync(tmpFilePath, 'utf-8');
                    
                    // Create a text edit to replace the entire document content
                    const fullRange = new vscode.Range(
                        document.positionAt(0),
                        document.positionAt(document.getText().length)
                    );
                    
                    // Clean up temporary file
                    fs.unlinkSync(tmpFilePath);
                    
                    // Return the edit
                    resolve([vscode.TextEdit.replace(fullRange, formattedText)]);
                } catch (readError) {
                    vscode.window.showErrorMessage(`Failed to read formatted content: ${readError.message}`);
                    resolve([]);
                }
            });
        } catch (writeError) {
            vscode.window.showErrorMessage(`Failed to create temporary file: ${writeError.message}`);
            resolve([]);
        }
    });
}
```

### 3. Adapting for Different Formatter Behaviors

Different formatters may have different behaviors. Here are some patterns you might need to adjust:

#### For formatters that output to stdout instead of modifying the file
```javascript
exec(`${formatCommand} "${tmpFilePath}"`, (error, stdout, stderr) => {
    if (error) {
        vscode.window.showErrorMessage(`Your Formatter error: ${stderr || error.message}`);
        return resolve([]);
    }
    
    // Use stdout instead of reading the file
    const formattedText = stdout;
    
    // Create a text edit to replace the entire document content
    const fullRange = new vscode.Range(
        document.positionAt(0),
        document.positionAt(document.getText().length)
    );
    
    // Clean up temporary file
    fs.unlinkSync(tmpFilePath);
    
    // Return the edit
    resolve([vscode.TextEdit.replace(fullRange, formattedText)]);
});
```

#### For formatters that require different command-line arguments
```javascript
// Example for a formatter that takes specific options
exec(`${formatCommand} --style=standard --quiet "${tmpFilePath}"`, (error, stdout, stderr) => {
    // ...
});
```

#### For formatters that process content differently
You might need to adjust how content is passed to the formatter. Some formatters accept content via stdin:

```javascript
const child = spawn(formatCommand, [/* args */]);
child.stdin.write(document.getText());
child.stdin.end();

let stdout = '';
child.stdout.on('data', (data) => {
    stdout += data;
});

child.on('close', (code) => {
    if (code === 0) {
        const fullRange = new vscode.Range(
            document.positionAt(0),
            document.positionAt(document.getText().length)
        );
        resolve([vscode.TextEdit.replace(fullRange, stdout)]);
    } else {
        vscode.window.showErrorMessage(`Formatter exited with code ${code}`);
        resolve([]);
    }
});
```

## Advanced Customization

### Adding Support for Format Selection
To add support for formatting only selected portions of a document:

```javascript
context.subscriptions.push(
    vscode.languages.registerDocumentRangeFormattingEditProvider(
        { language: 'python' }, // Change to your language
        {
            provideDocumentRangeFormattingEdits(document, range) {
                // Format only the selected range
                return formatDocumentRange(document, range);
            }
        }
    )
);

async function formatDocumentRange(document, range) {
    // Implementation for range formatting
    // This depends on whether your formatter supports range formatting
}
```

### Adding Commands with Arguments
To support additional commands with arguments:

```javascript
context.subscriptions.push(
    vscode.commands.registerCommand('your-formatter.formatWithOptions', () => {
        // Prompt user for options
        vscode.window.showQuickPick(['Option 1', 'Option 2']).then(option => {
            if (option) {
                // Format with the selected option
                // ...
            }
        });
    })
);
```

## Testing Your Customized Extension

1. Make your changes to both files
2. Run `npm install` if you've added dependencies
3. Press `F5` in VS Code to launch a debug session
4. Test the extension functionality
5. Package with `npm run package` when satisfied

## Examples

### Example: Python Black Formatter Extension

package.json:
```json
{
  "name": "black-formatter",
  "displayName": "Black Python Formatter",
  "description": "Format Python files using the Black formatter",
  "version": "0.1.0",
  "activationEvents": [
    "onLanguage:python"
  ],
  "contributes": {
    "commands": [
      {
        "command": "black-formatter.format",
        "title": "Format with Black"
      }
    ],
    "configuration": {
      "title": "Black Formatter",
      "properties": {
        "black-formatter.enableFormatOnSave": {
          "type": "boolean",
          "default": false,
          "description": "Enable formatting on save for Python files"
        },
        "black-formatter.formatCommand": {
          "type": "string",
          "default": "black",
          "description": "Command to execute Black"
        }
      }
    }
  }
}
```

extension.js:
```javascript
// Main changes to extension.js would be:
// 1. Change language checks to 'python'
// 2. Change the formatCommand default to 'black'
// 3. Update the command execution to match Black's parameters:
//    exec(`${formatCommand} "${tmpFilePath}"`, ...)
```