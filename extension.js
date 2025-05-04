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

    // Register command to set 42 username and email
    context.subscriptions.push(
        vscode.commands.registerCommand('c-formatter-42.set42info', async () => {
            const config = vscode.workspace.getConfiguration('c-formatter-42');
            
            // Ask for username (intra handle)
            const username = await vscode.window.showInputBox({
                prompt: 'Enter your 42 intra handle/username',
                placeHolder: 'e.g., jdoe',
                value: config.get('username', '')
            });
            
            if (username !== undefined) {
                // Ask for complete email address
                const email = await vscode.window.showInputBox({
                    prompt: 'Enter your complete 42 email address',
                    placeHolder: 'e.g., jdoe@student.42madrid.com',
                    value: config.get('email', '')
                });
                
                if (email !== undefined) {
                    // Save to settings
                    await config.update('username', username, true);
                    await config.update('email', email, true);
                    vscode.window.showInformationMessage('42 information saved successfully!');
                }
            }
        })
    );

    // Check if c_formatter_42 is installed
    checkFormatterInstallation();

    // Check if user has set 42 info
    checkUserInfo(context);

    // Setup format on save if enabled
    setupFormatOnSave(context);
}

/**
 * Check if user has set their 42 info
 * @param {vscode.ExtensionContext} context 
 */
function checkUserInfo(context) {
    const config = vscode.workspace.getConfiguration('c-formatter-42');
    const username = config.get('username', '');
    const email = config.get('email', '');
    
    if (!username || !email) {
        vscode.window.showInformationMessage(
            '42 intra handle or email not set. The header will be incorrect without this information.',
            'Set Now'
        ).then(selection => {
            if (selection === 'Set Now') {
                vscode.commands.executeCommand('c-formatter-42.set42info');
            }
        });
    }
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
        const formatCommand = config.get('formatCommand', 'c_formatter_42_wrapper');
        const enhancedMode = config.get('enhancedMode', true);
        
        // Use wrapper by default if available
        let commandToUse = formatCommand;
        
        // Check if the user has specified a custom executable via config
        const customExecutablePath = config.get('executablePath', null);
        if (customExecutablePath) {
            try {
                const stats = fs.statSync(customExecutablePath);
                if (stats.isFile()) {
                    commandToUse = customExecutablePath;
                }
            } catch (err) {
                // If the custom path doesn't exist, fall back to the default
                console.log(`Custom executable path not found: ${customExecutablePath}`);
            }
        }

        // Add enhanced mode flag if enabled
        let formatterArgs = [];
        if (enhancedMode) {
            formatterArgs.push('--enhanced');

            // Add username and email if provided
            const username = config.get('username', '');
            const email = config.get('email', '');
            
            if (username) {
                formatterArgs.push('--username', username);
            }
            
            if (email) {
                formatterArgs.push('--email', email);
            }
        }
        
        // Add wrapper verbose flag if debug mode is enabled
        if (config.get('debug', false)) {
            formatterArgs.push('--wrapper-verbose');
        }

        // Check if the formatter is available
        try {
            which.sync(commandToUse.split(' ')[0]);
        } catch (err) {
            vscode.window.showErrorMessage(
                `42 C Formatter: ${commandToUse} not found. Please install it with 'pip install c_formatter_42_wrapper'`
            );
            return resolve([]);
        }

        // Create a temporary file for passing content to c_formatter_42
        const tmpDir = os.tmpdir();
        const tmpFilePath = path.join(tmpDir, `vscode_42_format_${Date.now()}.c`);

        try {
            // Write current content to temporary file
            fs.writeFileSync(tmpFilePath, document.getText());

            // Execute the formatter on the temporary file
            // Set the environment variable to enable debug logging if configured
            const env = Object.assign({}, process.env);
            if (config.get('debug', false)) {
                env.C_FORMATTER_42_WRAPPER_DEBUG = "1";
                env.NORMINETTE_FORMATTER_DEBUG = "1";
            }
            
            // Add any custom environment variables
            const customEnv = config.get('environmentVariables', {});
            for (const [key, value] of Object.entries(customEnv)) {
                env[key] = value;
            }

            // Combine command and arguments
            const fullCommand = `${commandToUse} ${formatterArgs.join(' ')} "${tmpFilePath}"`;
            console.log(`Running formatter command: ${fullCommand}`);

            exec(fullCommand, { env }, (error, stdout, stderr) => {
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
 * Check if the formatter is installed and offer to install it if not
 */
function checkFormatterInstallation() {
    const config = vscode.workspace.getConfiguration('c-formatter-42');
    const formatCommand = config.get('formatCommand', 'c_formatter_42_wrapper').split(' ')[0];
    const installOnStartup = config.get('installOnStartup', false);
    
    try {
        which.sync(formatCommand);
        console.log(`42 C Formatter: ${formatCommand} found`);
    } catch (err) {
        if (installOnStartup) {
            const installCommand = 'pip install c_formatter_42_wrapper';
            
            vscode.window.showInformationMessage(
                `42 C Formatter: ${formatCommand} not found. Installing...`,
            );
            
            try {
                execSync(installCommand, { stdio: 'inherit' });
                vscode.window.showInformationMessage('42 C Formatter: Installation completed successfully');
            } catch (installErr) {
                vscode.window.showErrorMessage(
                    `Failed to install c_formatter_42_wrapper. Please install manually with '${installCommand}'`,
                );
            }
        } else {
            vscode.window.showInformationMessage(
                `42 C Formatter: ${formatCommand} not found. Please install it with 'pip install c_formatter_42_wrapper'`,
                'Install Now', 'Ignore'
            ).then(selection => {
                if (selection === 'Install Now') {
                    const terminal = vscode.window.createTerminal('42 C Formatter Installation');
                    terminal.sendText('pip install c_formatter_42_wrapper');
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