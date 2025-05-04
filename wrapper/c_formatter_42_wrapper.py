#!/usr/bin/env python3
"""
c_formatter_42 Wrapper

This script is a wrapper around the c_formatter_42 formatter that addresses Python
environment compatibility issues, particularly when used in IDE extensions.

Features:
- Multiple detection methods for finding the correct c_formatter_42 installation
- Environment variable configuration (C_FORMATTER_42_PATH)
- Support for pipx, virtualenv, and system installations
- Fall back mechanisms for ensuring the formatter is always found
- Enhanced norminette compliance fixing additional issues

Usage:
  c_formatter_42_wrapper.py [options] [file ...]
  
  Same options as c_formatter_42 plus:
  --enhanced        Use enhanced formatter with full norminette compliance
  --wrapper-verbose Enable verbose logging
  --wrapper-path    Print the path to the formatter and exit
  --username        Specify 42 intra handle for header
  --email           Specify 42 email for header
"""

import os
import sys
import subprocess
import shutil
import importlib.util
import argparse
import tempfile
import site
import logging
from pathlib import Path
from typing import List, Optional, Tuple, Any

# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger("c_formatter_42_wrapper")

# Check for DEBUG environment variable
if os.environ.get("C_FORMATTER_42_WRAPPER_DEBUG", "").lower() in ("1", "true", "yes"):
    logger.setLevel(logging.DEBUG)

def find_executable(name: str) -> Optional[str]:
    """Find the path to an executable using 'which' or similar commands"""
    try:
        return shutil.which(name)
    except Exception:
        return None

def find_formatter_module() -> Optional[str]:
    """Try to import the c_formatter_42 module and return its location"""
    try:
        spec = importlib.util.find_spec("c_formatter_42")
        if spec and spec.origin:
            return os.path.dirname(os.path.dirname(spec.origin))
        return None
    except (ImportError, AttributeError):
        return None

def find_user_site_bin() -> Optional[str]:
    """Find the user site-packages bin directory"""
    try:
        user_base = site.USER_BASE
        if user_base:
            # Check common locations based on the user_base
            potential_paths = [
                os.path.join(user_base, "bin"),  # Unix/Mac
                os.path.join(user_base, "Scripts"),  # Windows
            ]
            
            for path in potential_paths:
                if os.path.exists(path):
                    return path
    except Exception:
        pass
    return None

def find_virtual_env() -> Optional[str]:
    """Check if running in a virtual environment and return the bin path"""
    if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix):
        # We're in a virtualenv or venv
        if sys.platform == "win32":
            return os.path.join(sys.prefix, "Scripts")
        else:
            return os.path.join(sys.prefix, "bin")
    return None

def find_pipx_bin() -> Optional[str]:
    """Find pipx bin directory"""
    # Common pipx locations
    potential_paths = [
        os.path.expanduser("~/.local/bin"),
        os.path.expanduser("~/.local/pipx/venvs/c-formatter-42/bin"),
    ]
    
    for path in potential_paths:
        if os.path.exists(path) and os.path.exists(os.path.join(path, "c_formatter_42")):
            return path
    return None

def find_brew_cellar() -> Optional[str]:
    """Find homebrew cellar path for c_formatter_42"""
    try:
        # Check if brew is available
        if find_executable("brew"):
            # Try to locate c_formatter_42 in Homebrew cellar
            result = subprocess.run(
                ["brew", "--prefix", "c-formatter-42"],
                capture_output=True, text=True, check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                return os.path.join(result.stdout.strip(), "bin")
    except Exception:
        pass
    return None

def run_formatter_cmd(formatter_path: str, args: List[str]) -> int:
    """Run the formatter with the given arguments"""
    logger.debug(f"Running formatter: {formatter_path} {' '.join(args)}")
    try:
        result = subprocess.run([formatter_path] + args, check=False)
        return result.returncode
    except Exception as e:
        logger.error(f"Error running formatter: {e}")
        return 1

def run_formatter_module(module_path: str, args: List[str]) -> int:
    """Run the formatter module using the Python interpreter"""
    python_exe = sys.executable
    logger.debug(f"Running formatter module: {python_exe} -m c_formatter_42 {' '.join(args)}")
    try:
        if module_path:
            env = os.environ.copy()
            env["PYTHONPATH"] = module_path + ":" + env.get("PYTHONPATH", "")
            result = subprocess.run([python_exe, "-m", "c_formatter_42"] + args, env=env, check=False)
        else:
            result = subprocess.run([python_exe, "-m", "c_formatter_42"] + args, check=False)
        return result.returncode
    except Exception as e:
        logger.error(f"Error running formatter module: {e}")
        return 1

def create_temp_wrapper_script(module_path: Optional[str] = None) -> Tuple[str, str]:
    """Create a temporary wrapper script that correctly imports and runs c_formatter_42"""
    fd, temp_path = tempfile.mkstemp(suffix=".py", prefix="c_formatter_42_wrapper_")
    
    script_content = f"""#!/usr/bin/env python3
import os
import sys

"""
    
    if module_path:
        script_content += f"""# Add the module path to Python path
sys.path.insert(0, "{module_path}")
"""
    
    script_content += """try:
    from c_formatter_42.__main__ import main
    sys.exit(main())
except ImportError as e:
    print(f"Error importing c_formatter_42: {e}", file=sys.stderr)
    sys.exit(1)
"""
    
    with os.fdopen(fd, 'w') as f:
        f.write(script_content)
    
    # Make the script executable
    os.chmod(temp_path, 0o755)
    
    # Create a name for the temp file that looks like the original formatter
    temp_dir = os.path.dirname(temp_path)
    temp_name = os.path.join(temp_dir, "c_formatter_42")
    
    # On Windows, add .py extension
    if sys.platform == "win32":
        temp_name += ".py"
    
    # Create a symlink or copy the file if symlinks are not supported
    try:
        if hasattr(os, 'symlink'):
            if os.path.exists(temp_name):
                os.unlink(temp_name)
            os.symlink(temp_path, temp_name)
        else:
            shutil.copy2(temp_path, temp_name)
    except Exception:
        # If we can't create a symlink or copy, just use the original name
        temp_name = temp_path
    
    return temp_path, temp_name

def cleanup_temp_files(temp_path: str, temp_name: str) -> None:
    """Clean up the temporary files created"""
    try:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        if temp_name != temp_path and os.path.exists(temp_name):
            os.unlink(temp_name)
    except Exception as e:
        logger.warning(f"Error cleaning up temporary files: {e}")

def find_formatter() -> Tuple[Optional[str], Optional[str], str]:
    """
    Find the c_formatter_42 formatter executable or module
    
    Returns:
        tuple: (executable_path, module_path, method)
            executable_path: Path to the executable (if found)
            module_path: Path to the module (if found)
            method: Method to use ('executable', 'module', or 'wrapper')
    """
    # 1. Check environment variable first (highest priority)
    env_path = os.environ.get("C_FORMATTER_42_PATH")
    if env_path:
        logger.debug(f"Found C_FORMATTER_42_PATH environment variable: {env_path}")
        # Check if it's an executable or a directory
        if os.path.isfile(env_path) and os.access(env_path, os.X_OK):
            return env_path, None, "executable"
        elif os.path.isdir(env_path):
            # Check if it's a Python package
            if os.path.exists(os.path.join(env_path, "c_formatter_42", "__init__.py")):
                return None, env_path, "module"
            # Check if there's an executable in the directory
            executable = os.path.join(env_path, "c_formatter_42")
            if os.path.isfile(executable) and os.access(executable, os.X_OK):
                return executable, None, "executable"
    
    # 2. Try to find the executable in PATH
    executable = find_executable("c_formatter_42")
    if executable:
        logger.debug(f"Found c_formatter_42 executable in PATH: {executable}")
        return executable, None, "executable"
    
    # 3. Try to find the module
    module_path = find_formatter_module()
    if module_path:
        logger.debug(f"Found c_formatter_42 module: {module_path}")
        return None, module_path, "module"
    
    # 4. Check pipx installation
    pipx_bin = find_pipx_bin()
    if pipx_bin:
        executable = os.path.join(pipx_bin, "c_formatter_42")
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            logger.debug(f"Found c_formatter_42 in pipx: {executable}")
            return executable, None, "executable"
    
    # 5. Check user site-packages bin
    user_bin = find_user_site_bin()
    if user_bin:
        executable = os.path.join(user_bin, "c_formatter_42")
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            logger.debug(f"Found c_formatter_42 in user site-packages: {executable}")
            return executable, None, "executable"
    
    # 6. Check virtual environment
    venv_bin = find_virtual_env()
    if venv_bin:
        executable = os.path.join(venv_bin, "c_formatter_42")
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            logger.debug(f"Found c_formatter_42 in virtual environment: {executable}")
            return executable, None, "executable"
    
    # 7. Check Homebrew cellar
    brew_bin = find_brew_cellar()
    if brew_bin:
        executable = os.path.join(brew_bin, "c_formatter_42")
        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            logger.debug(f"Found c_formatter_42 in Homebrew: {executable}")
            return executable, None, "executable"
    
    # 8. Last resort: try to run 'which' command directly
    try:
        result = subprocess.run(
            ["which", "c_formatter_42"],
            capture_output=True, text=True, check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            executable = result.stdout.strip()
            logger.debug(f"Found c_formatter_42 using 'which' command: {executable}")
            return executable, None, "executable"
    except Exception:
        pass
    
    # If we have a module path but no executable, we can still use it
    if module_path:
        return None, module_path, "wrapper"
    
    # Nothing found
    logger.error("Could not find c_formatter_42 installation")
    return None, None, "none"

def find_enhanced_formatter() -> Optional[str]:
    """Find the enhanced norminette formatter"""
    # Look for norminette_formatter.py in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    formatter_path = os.path.join(script_dir, "norminette_formatter.py")
    
    if os.path.exists(formatter_path):
        # Make sure it's executable
        try:
            os.chmod(formatter_path, 0o755)
        except Exception:
            pass
        return formatter_path
    
    return None

def run_enhanced_formatter(filepaths: List[str], args: List[str]) -> int:
    """Run the enhanced norminette formatter"""
    formatter_path = find_enhanced_formatter()
    if not formatter_path:
        logger.error("Enhanced formatter not found")
        return 1
    
    try:
        # Run the enhanced formatter
        cmd = [sys.executable, formatter_path] + args + filepaths
        logger.debug(f"Running enhanced formatter: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        logger.error(f"Error running enhanced formatter: {e}")
        return 1

def main():
    """Main function"""
    # Parse command-line arguments to pass to the formatter
    parser = argparse.ArgumentParser(add_help=False)
    # Add a new --wrapper-verbose flag just for our wrapper
    parser.add_argument("--wrapper-verbose", action="store_true", help=argparse.SUPPRESS)
    # Add a new --wrapper-path flag to print the path and exit
    parser.add_argument("--wrapper-path", action="store_true", help=argparse.SUPPRESS)
    # Add an enhanced mode flag
    parser.add_argument("--enhanced", action="store_true", help=argparse.SUPPRESS)
    # Add username and email options
    parser.add_argument("--username", type=str, help=argparse.SUPPRESS)
    parser.add_argument("--email", type=str, help=argparse.SUPPRESS)
    
    # Do a first pass to check for our custom flags
    args, remaining = parser.parse_known_args()
    
    # If verbose flag is set, enable debug logging
    if args.wrapper_verbose:
        logger.setLevel(logging.DEBUG)
    
    # Find the formatter
    executable_path, module_path, method = find_formatter()
    
    # If --wrapper-path is set, print the path and exit
    if args.wrapper_path:
        if executable_path:
            print(f"Executable: {executable_path}")
        if module_path:
            print(f"Module: {module_path}")
        print(f"Method: {method}")
        
        # Also check for enhanced formatter
        enhanced_path = find_enhanced_formatter()
        if enhanced_path:
            print(f"Enhanced formatter: {enhanced_path}")
        else:
            print("Enhanced formatter: Not found")
        
        return 0
    
    # If enhanced mode is requested, use the enhanced formatter
    if args.enhanced:
        # Extract the file paths from remaining args (last arguments)
        filepaths = [arg for arg in remaining if not arg.startswith('-')]
        args_flags = [arg for arg in remaining if arg.startswith('-')]
        
        # Add username and email flags if provided
        if args.username:
            args_flags.extend(["--username", args.username])
        if args.email:
            args_flags.extend(["--email", args.email])
        
        return run_enhanced_formatter(filepaths, args_flags)
    
    # Check if we found the formatter
    if method == "none":
        print("Error: c_formatter_42 not found. Please install it using one of the following methods:")
        print("  pip install c_formatter_42")
        print("  pipx install c_formatter_42")
        print("  brew install c-formatter-42 (on macOS with Homebrew)")
        print("\nOr set the C_FORMATTER_42_PATH environment variable to the path of the executable.")
        return 1
    
    # Run the formatter with the provided arguments
    if method == "executable":
        return run_formatter_cmd(executable_path, remaining)
    elif method == "module":
        return run_formatter_module(module_path, remaining)
    elif method == "wrapper":
        # Create a temporary wrapper script
        temp_path, temp_name = create_temp_wrapper_script(module_path)
        try:
            return run_formatter_cmd(temp_name, remaining)
        finally:
            cleanup_temp_files(temp_path, temp_name)
    
    # Should never reach here
    return 1

if __name__ == "__main__":
    sys.exit(main())
