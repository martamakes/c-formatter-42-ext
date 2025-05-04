# Common VSCode Extension Patterns and Examples

This document provides practical examples of common patterns and use cases for VSCode extensions. These examples can serve as a reference when developing your own extension.

## Table of Contents

1. [Commands and Menus](#commands-and-menus)
2. [Extension Settings](#extension-settings)
3. [File and Editor Operations](#file-and-editor-operations)
4. [External Tools Integration](#external-tools-integration)
5. [UI Components](#ui-components)
6. [Language Features](#language-features)
7. [Workspace Manipulation](#workspace-manipulation)

## Commands and Menus

### Registering a Basic Command

```javascript
function activate(context) {
  // Register a simple command
  let disposable = vscode.commands.registerCommand('myextension.helloWorld', function () {
    vscode.window.showInformationMessage('Hello World from My Extension!');
  });
  
  context.subscriptions.push(disposable);
}
```

### Adding a Command to Context Menu

In your package.json:

```json
"contributes": {
  "commands": [
    {
      "command": "myextension.contextAction",
      "title": "Do Something with Selection"
    }
  ],
  "menus": {
    "editor/context": [
      {
        "command": "myextension.contextAction",
        "when": "editorHasSelection"
      }
    ]
  }
}
```

## Extension Settings

### Adding Custom Settings

In package.json:

```json
"contributes": {
  "configuration": {
    "title": "My Extension",
    "properties": {
      "myextension.enableFeature": {
        "type": "boolean",
        "default": true,
        "description": "Enable the special feature"
      },
      "myextension.optionList": {
        "type": "string",
        "enum": ["option1", "option2", "option3"],
        "default": "option1",
        "description": "Select from available options"
      }
    }
  }
}
```

### Reading Settings in Code

```javascript
function getSettings() {
  const config = vscode.workspace.getConfiguration('myextension');
  const isFeatureEnabled = config.get('enableFeature');
  const selectedOption = config.get('optionList');
  
  return { isFeatureEnabled, selectedOption };
}
```

### Updating Settings

```javascript
async function toggleFeature() {
  const config = vscode.workspace.getConfiguration('myextension');
  const currentValue = config.get('enableFeature');
  
  await config.update('enableFeature', !currentValue, true);
  vscode.window.showInformationMessage(`Feature is now ${!currentValue ? 'enabled' : 'disabled'}`);
}
```

## File and Editor Operations

### Getting Active Editor Content

```javascript
function getEditorContent() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor!');
    return null;
  }
  
  return editor.document.getText();
}
```

### Modifying Editor Content

```javascript
function replaceSelection() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    return;
  }
  
  const selection = editor.selection;
  
  editor.edit(editBuilder => {
    editBuilder.replace(selection, 'New Text');
  });
}
```

### Working with Files

```javascript
async function readAndWriteFile() {
  try {
    // Read file
    const uri = vscode.Uri.file('/path/to/file.txt');
    const content = await vscode.workspace.fs.readFile(uri);
    const text = Buffer.from(content).toString('utf8');
    
    // Process content
    const modifiedText = text.toUpperCase();
    
    // Write back to file
    const encodedContent = Buffer.from(modifiedText, 'utf8');
    await vscode.workspace.fs.writeFile(uri, encodedContent);
    
    vscode.window.showInformationMessage('File processed successfully!');
  } catch (error) {
    vscode.window.showErrorMessage(`Error processing file: ${error.message}`);
  }
}
```

## External Tools Integration

### Running External Commands

```javascript
const { exec } = require('child_process');

function runExternalTool(command) {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        reject(error);
        return;
      }
      resolve(stdout.trim());
    });
  });
}

async function formatWithExternalTool() {
  try {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      return;
    }
    
    const document = editor.document;
    const filePath = document.uri.fsPath;
    
    // Run external formatter
    await runExternalTool(`prettier --write "${filePath}"`);
    
    // Refresh the document
    await document.save();
    
    vscode.window.showInformationMessage('File formatted successfully!');
  } catch (error) {
    vscode.window.showErrorMessage(`Formatting failed: ${error.message}`);
  }
}
```

### Creating a Formatter Extension

```javascript
function activate(context) {
  // Register a document formatter for JavaScript files
  const formatter = {
    provideDocumentFormattingEdits(document) {
      // Use an external formatting tool or your own formatting logic
      const text = document.getText();
      const formattedText = yourFormattingFunction(text);
      
      const fullRange = new vscode.Range(
        document.positionAt(0),
        document.positionAt(text.length)
      );
      
      return [vscode.TextEdit.replace(fullRange, formattedText)];
    }
  };
  
  context.subscriptions.push(
    vscode.languages.registerDocumentFormattingEditProvider(
      { language: 'javascript' },
      formatter
    )
  );
}
```

## UI Components

### Status Bar Item

```javascript
function createStatusBarItem(context) {
  const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
  );
  
  statusBarItem.text = "$(symbol-event) Ready";
  statusBarItem.tooltip = "My Extension Status";
  statusBarItem.command = "myextension.statusClicked";
  statusBarItem.show();
  
  context.subscriptions.push(statusBarItem);
  
  // Register the command for when status bar is clicked
  context.subscriptions.push(
    vscode.commands.registerCommand("myextension.statusClicked", () => {
      vscode.window.showInformationMessage("Status bar clicked!");
    })
  );
  
  return statusBarItem;
}
```

### Creating a WebView Panel

```javascript
function createWebViewPanel() {
  const panel = vscode.window.createWebviewPanel(
    'myWebview',
    'My Webview',
    vscode.ViewColumn.One,
    {
      enableScripts: true,
      retainContextWhenHidden: true
    }
  );
  
  // Set webview content
  panel.webview.html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>My Extension Webview</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        button { padding: 8px 16px; margin-top: 20px; }
      </style>
    </head>
    <body>
      <h1>Hello from Webview</h1>
      <p>This is a custom UI panel created by my extension.</p>
      <button id="actionBtn">Click Me</button>
      
      <script>
        const vscode = acquireVsCodeApi();
        document.getElementById('actionBtn').addEventListener('click', () => {
          vscode.postMessage({ command: 'alert', text: 'Button clicked!' });
        });
      </script>
    </body>
    </html>
  `;
  
  // Handle messages from the webview
  panel.webview.onDidReceiveMessage(
    message => {
      switch (message.command) {
        case 'alert':
          vscode.window.showInformationMessage(message.text);
          return;
      }
    }
  );
  
  return panel;
}
```

## Language Features

### Code Completion Provider

```javascript
function registerCompletionProvider(context) {
  const provider = {
    provideCompletionItems(document, position) {
      // Create a list of completion items
      const completionItems = [];
      
      // Add a simple completion item
      const simpleCompletion = new vscode.CompletionItem('console.log');
      simpleCompletion.kind = vscode.CompletionItemKind.Method;
      simpleCompletion.insertText = 'console.log($1);';
      simpleCompletion.documentation = new vscode.MarkdownString('Log to the console');
      simpleCompletion.insertTextRules = vscode.CompletionItemInsertTextRule.InsertAsSnippet;
      
      completionItems.push(simpleCompletion);
      
      return completionItems;
    }
  };
  
  context.subscriptions.push(
    vscode.languages.registerCompletionItemProvider(
      { language: 'javascript' },
      provider,
      '.' // Trigger character
    )
  );
}
```

### Diagnostics (Error/Warning Highlighting)

```javascript
function provideDiagnostics(context) {
  // Create diagnostics collection
  const diagnosticCollection = vscode.languages.createDiagnosticCollection('my-extension');
  context.subscriptions.push(diagnosticCollection);
  
  // Update diagnostics when a file is opened or changed
  context.subscriptions.push(
    vscode.workspace.onDidOpenTextDocument(updateDiagnostics),
    vscode.workspace.onDidChangeTextDocument(e => updateDiagnostics(e.document))
  );
  
  // Initial update for all open documents
  vscode.workspace.textDocuments.forEach(updateDiagnostics);
  
  function updateDiagnostics(document) {
    if (document.languageId !== 'javascript') {
      return;
    }
    
    const text = document.getText();
    const diagnostics = [];
    
    // Example: Flag all uses of `var` keywords
    const varRegex = /\bvar\s+([a-zA-Z_]\w*)/g;
    let match;
    
    while ((match = varRegex.exec(text))) {
      const position = document.positionAt(match.index);
      const range = new vscode.Range(
        position,
        document.positionAt(match.index + match[0].length)
      );
      
      const diagnostic = new vscode.Diagnostic(
        range,
        `Consider using 'let' or 'const' instead of 'var'`,
        vscode.DiagnosticSeverity.Warning
      );
      
      diagnostics.push(diagnostic);
    }
    
    diagnosticCollection.set(document.uri, diagnostics);
  }
}
```

## Workspace Manipulation

### File System Watcher

```javascript
function watchWorkspaceFiles(context) {
  // Watch for all JavaScript file changes in the workspace
  const fileWatcher = vscode.workspace.createFileSystemWatcher(
    '**/*.js',
    false, // Don't ignore file creation events
    false, // Don't ignore file change events
    false  // Don't ignore file deletion events
  );
  
  // Register event handlers
  context.subscriptions.push(
    fileWatcher,
    fileWatcher.onDidCreate(uri => {
      vscode.window.showInformationMessage(`File created: ${uri.fsPath}`);
    }),
    fileWatcher.onDidChange(uri => {
      console.log(`File changed: ${uri.fsPath}`);
    }),
    fileWatcher.onDidDelete(uri => {
      vscode.window.showWarningMessage(`File deleted: ${uri.fsPath}`);
    })
  );
}
```

### Working with Workspaces

```javascript
async function listWorkspaceFiles() {
  if (!vscode.workspace.workspaceFolders) {
    vscode.window.showInformationMessage('No workspace is open');
    return;
  }
  
  // Get the first workspace folder
  const workspaceFolder = vscode.workspace.workspaceFolders[0];
  
  try {
    // Find all JavaScript files in the workspace
    const pattern = new vscode.RelativePattern(workspaceFolder, '**/*.js');
    const files = await vscode.workspace.findFiles(pattern, '**/node_modules/**');
    
    // Show results
    if (files.length === 0) {
      vscode.window.showInformationMessage('No JavaScript files found');
    } else {
      vscode.window.showInformationMessage(`Found ${files.length} JavaScript files`);
      
      // Do something with the files
      // ...
    }
  } catch (error) {
    vscode.window.showErrorMessage(`Error listing files: ${error.message}`);
  }
}
```

Remember that these patterns are just examples to get you started. VSCode's extension API is extensive, and there are many more possibilities depending on your specific needs.

For the most up-to-date and detailed information, always refer to the [official VS Code Extension API documentation](https://code.visualstudio.com/api).