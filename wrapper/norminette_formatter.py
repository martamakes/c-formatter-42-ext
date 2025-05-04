#!/usr/bin/env python3
"""
Norminette Formatter

This script extends c_formatter_42 to address additional norminette requirements:
- Adds 42 header if missing
- Fixes space vs tab issues
- Separates variable declaration and initialization
- Adds newlines after variable declarations
- Ensures braces are followed by newlines
- Adds newlines at end of files

Usage:
  norminette_formatter.py [options] [file ...]
"""

import os
import sys
import re
import subprocess
import tempfile
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any

# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger("norminette_formatter")

# Check for DEBUG environment variable
if os.environ.get("NORMINETTE_FORMATTER_DEBUG", "").lower() in ("1", "true", "yes"):
    logger.setLevel(logging.DEBUG)

# Constants
HEADER_TEMPLATE = """/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   {filename}                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: {username} <{email}>                        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: {created_date} by {username}            #+#    #+#             */
/*   Updated: {updated_date} by {username}           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

"""

def get_header_info(custom_username=None, custom_email=None) -> Dict[str, str]:
    """Get information for the 42 header"""
    # Try to get username from environment or custom value
    username = custom_username or os.environ.get("USER", "unknown")
    
    # Try to get email from git config or custom value
    email = custom_email or "unknown@student.42.fr"
    if not custom_email:
        try:
            email_proc = subprocess.run(
                ["git", "config", "user.email"],
                capture_output=True, text=True, check=False
            )
            if email_proc.returncode == 0 and email_proc.stdout.strip():
                email = email_proc.stdout.strip()
        except Exception:
            pass
    
    # If we couldn't get email from git, try to guess based on username
    if email == "unknown@student.42.fr" and username != "unknown":
        email = f"{username}@student.42.fr"
    
    # Get current date in the format YYYY/MM/DD HH:MM:SS
    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d %H:%M:%S")
    
    return {
        "username": username,
        "email": email,
        "created_date": date_str,
        "updated_date": date_str
    }

def add_header(content: str, filename: str, custom_username=None, custom_email=None) -> str:
    """Add 42 header to the file if missing"""
    # Check if content already has a 42 header
    if "/* ************************************************************************** */" in content:
        return content
    
    # Get header info
    header_info = get_header_info(custom_username, custom_email)
    
    # Create the header using the template
    header = HEADER_TEMPLATE.format(
        filename=os.path.basename(filename).ljust(51),  # Filename padded to 51 chars
        username=header_info["username"],
        email=header_info["email"],
        created_date=header_info["created_date"],
        updated_date=header_info["updated_date"]
    )
    
    # Add header to the content
    return header + content

def fix_tabs_spaces(content: str) -> str:
    """Fix tabs and spaces according to norminette"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Replace leading spaces with tabs for indentation
        leading_space_count = len(line) - len(line.lstrip(' '))
        if leading_space_count > 0:
            tab_count = leading_space_count // 4  # Assuming 4 spaces per tab
            remaining_spaces = leading_space_count % 4
            fixed_line = '\t' * tab_count + ' ' * remaining_spaces + line.lstrip(' ')
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_variable_declaration(content: str) -> str:
    """Separate variable declaration and initialization"""
    lines = content.split('\n')
    fixed_lines = []
    
    # Regular expressions to match variable declarations with initialization
    var_init_re = re.compile(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+);$')
    
    for line in lines:
        match = var_init_re.match(line)
        if match:
            # Found a variable declaration with initialization
            indent, declaration, value = match.groups()
            # Create separate declaration and assignment
            fixed_lines.append(f"{indent}{declaration};")
            fixed_lines.append(f"{indent}{declaration.split()[-1]} = {value};")
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def add_newlines_after_var_decl(content: str) -> str:
    """Add newlines after variable declarations"""
    lines = content.split('\n')
    fixed_lines = []
    
    # Regular expression to match variable declarations
    var_decl_re = re.compile(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*);$')
    
    for i, line in enumerate(lines):
        fixed_lines.append(line)
        
        # If this is a variable declaration and the next line is not empty
        if var_decl_re.match(line) and i < len(lines) - 1 and lines[i+1].strip():
            fixed_lines.append('')
    
    return '\n'.join(fixed_lines)

def fix_braces_newlines(content: str) -> str:
    """Ensure braces are followed by newlines"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_lines.append(line)
        
        # If this line ends with a brace and the next line is not empty
        if (line.strip().endswith('{') or line.strip() == '{') and \
           i < len(lines) - 1 and lines[i+1].strip():
            fixed_lines.append('')
    
    return '\n'.join(fixed_lines)

def ensure_newline_at_eof(content: str) -> str:
    """Ensure the file ends with a newline"""
    if not content.endswith('\n'):
        return content + '\n'
    return content

def run_c_formatter_42(content: str, filename: str) -> str:
    """Run c_formatter_42 on the content"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.c', delete=False) as tmp_file:
        tmp_file_path = tmp_file.name
        tmp_file.write(content)
    
    try:
        # Try to run c_formatter_42 on the temporary file
        subprocess.run(
            ["c_formatter_42_wrapper", tmp_file_path],
            check=True
        )
        
        # Read the formatted content
        with open(tmp_file_path, 'r') as file:
            formatted_content = file.read()
        
        return formatted_content
    except Exception as e:
        logger.error(f"Error running c_formatter_42: {e}")
        return content
    finally:
        # Clean up the temporary file
        try:
            os.unlink(tmp_file_path)
        except Exception:
            pass

def apply_full_formatting(content: str, filename: str, custom_username=None, custom_email=None) -> str:
    """Apply all formatting rules"""
    # First use c_formatter_42 for basic formatting
    content = run_c_formatter_42(content, filename)
    
    # Then apply additional norminette fixes
    content = add_header(content, filename, custom_username, custom_email)
    content = fix_tabs_spaces(content)
    content = fix_variable_declaration(content)
    content = add_newlines_after_var_decl(content)
    content = fix_braces_newlines(content)
    content = ensure_newline_at_eof(content)
    
    return content

def main() -> int:
    """Main function"""
    parser = argparse.ArgumentParser(
        prog="norminette_formatter",
        description="Format C files according to 42 norminette rules",
    )
    parser.add_argument(
        "-c", "--confirm",
        action="store_true",
        help="Ask confirmation before overwriting any file",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Skip adding the 42 header",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--username",
        type=str,
        help="Custom username for 42 header",
    )
    parser.add_argument(
        "--email",
        type=str,
        help="Custom email for 42 header",
    )
    parser.add_argument(
        "filepaths",
        metavar="FILE",
        nargs="*",
        help="File to format inplace, if no file is provided read STDIN",
    )
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    if len(args.filepaths) == 0:
        # Read from STDIN
        content = sys.stdin.read()
        formatted = apply_full_formatting(content, "stdin.c", args.username, args.email)
        print(formatted, end="")
        return 0
    
    for filepath in args.filepaths:
        try:
            # Read file content
            with open(filepath, "r") as file:
                content = file.read()
            
            # Format the content
            if args.no_header:
                # Skip adding header but apply other fixes
                content = run_c_formatter_42(content, filepath)
                content = fix_tabs_spaces(content)
                content = fix_variable_declaration(content)
                content = add_newlines_after_var_decl(content)
                content = fix_braces_newlines(content)
                content = ensure_newline_at_eof(content)
            else:
                content = apply_full_formatting(content, filepath, args.username, args.email)
            
            # Ask for confirmation if requested
            if args.confirm:
                result = input(f"Are you sure you want to overwrite {filepath}? [y/N] ")
                if result.lower() != "y":
                    continue
            
            # Write the formatted content back to the file
            print(f"Writing to {filepath}")
            with open(filepath, "w") as file:
                file.write(content)
        
        except OSError as e:
            print(f"Error: {e.filename}: {e.strerror}", file=sys.stderr)
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
