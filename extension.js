const vscode = require('vscode');
const { exec, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const which = require('which');
const os = require('os');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('42 C Formatter extension is now active');

    // Register the formatter provider
    const formatterProvider = {
        provideDocumentFormattingEdits(document) {
            if (document.languageId !== 'c') {
                return [];
            }
            
            return formatDocument(document);
        }
    };

    // Register the document formatter for C files
    context.subscriptions.push(
        vscode.languages.registerDocumentFormattingEditProvider(
            { language: 'c' },
            formatterProvider
        )
    );

    // Register the format command
    context.subscriptions.push(
        vscode.commands.registerCommand('c-formatter-42.format', () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'c') {
                vscode.window.showErrorMessage('This command only works with C files');
                return;
            }

            vscode.commands.executeCommand('editor.action.formatDocument');
        })
    );

    // Check if c_formatter_42 is installed
    checkFormatterInstallation();

    // Setup format on save if enabled
    setupFormatOnSave(context);
}

/**
 * Format the document using c_formatter_42
 * @param {vscode.TextDocument} document 
 * @returns {Promise<vscode.TextEdit[]>}
 */
async function formatDocument(document) {
    return new Promise((resolve, reject) => {
        // Get the configuration
        const config = vscode.workspace.getConfiguration('c-formatter-42');
        const formatCommand = config.get('formatCommand', 'c_formatter_42');

        // Check if c_formatter_42 is available
        try {
            which.sync(formatCommand.split(' ')[0]);
        } catch (err) {
            vscode.window.showErrorMessage(
                `42 C Formatter: ${formatCommand} not found. Please install it with 'pip install c_formatter_42'`
            );
            return resolve([]);
        }

        // Create a temporary file for passing content to c_formatter_42
        const tmpDir = os.tmpdir();
        const tmpFilePath = path.join(tmpDir, `vscode_42_format_${Date.now()}.c`);

        try {
            // Write current content to temporary file
            fs.writeFileSync(tmpFilePath, document.getText());

            // Execute c_formatter_42 on the temporary file
            exec(`${formatCommand} "${tmpFilePath}"`, (error, stdout, stderr) => {
                try {
                    if (error) {
                        vscode.window.showErrorMessage(`42 C Formatter error: ${stderr || error.message}`);
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

/**
 * Check if c_formatter_42 is installed and offer to install it if not
 */
function checkFormatterInstallation() {
    const config = vscode.workspace.getConfiguration('c-formatter-42');
    const formatCommand = config.get('formatCommand', 'c_formatter_42').split(' ')[0];
    const installOnStartup = config.get('installOnStartup', false);
    
    try {
        which.sync(formatCommand);
        console.log(`42 C Formatter: ${formatCommand} found`);
    } catch (err) {
        if (installOnStartup) {
            const installCommand = 'pip install c_formatter_42';
            
            vscode.window.showInformationMessage(
                `42 C Formatter: ${formatCommand} not found. Installing...`,
            );
            
            try {
                execSync(installCommand, { stdio: 'inherit' });
                vscode.window.showInformationMessage('42 C Formatter: Installation completed successfully');
            } catch (installErr) {
                vscode.window.showErrorMessage(
                    `Failed to install c_formatter_42. Please install manually with '${installCommand}'`,
                );
            }
        } else {
            vscode.window.showInformationMessage(
                `42 C Formatter: ${formatCommand} not found. Please install it with 'pip install c_formatter_42'`,
                'Install Now', 'Ignore'
            ).then(selection => {
                if (selection === 'Install Now') {
                    const terminal = vscode.window.createTerminal('42 C Formatter Installation');
                    terminal.sendText('pip install c_formatter_42');
                    terminal.show();
                }
            });
        }
    }
}

/**
 * Set up format on save if enabled
 * @param {vscode.ExtensionContext} context 
 */
function setupFormatOnSave(context) {
    const config = vscode.workspace.getConfiguration('c-formatter-42');
    const enableFormatOnSave = config.get('enableFormatOnSave', false);
    
    if (enableFormatOnSave) {
        context.subscriptions.push(
            vscode.workspace.onWillSaveTextDocument(event => {
                if (event.document.languageId === 'c') {
                    event.waitUntil(
                        vscode.commands.executeCommand('editor.action.formatDocument')
                    );
                }
            })
        );
    }
    
    // Listen for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(event => {
            if (event.affectsConfiguration('c-formatter-42.enableFormatOnSave')) {
                // Reload the extension to apply new settings
                vscode.commands.executeCommand('workbench.action.reloadWindow');
            }
        })
    );
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};