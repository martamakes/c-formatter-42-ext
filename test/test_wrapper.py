#!/usr/bin/env python3
"""
Test script for the c_formatter_42_wrapper

This script tests the wrapper's ability to find and use the c_formatter_42
formatter in various environments.
"""

import os
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

# Add the wrapper directory to the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "wrapper"))

try:
    from c_formatter_42_wrapper import (
        find_formatter,
        find_executable,
        find_formatter_module,
        find_virtual_env,
        find_pipx_bin,
        find_user_site_bin,
    )
except ImportError:
    print("Could not import c_formatter_42_wrapper. Make sure it's in the path.")
    sys.exit(1)


class TestWrapper(unittest.TestCase):
    """Tests for the c_formatter_42_wrapper"""

    def setUp(self):
        # Save original environment
        self.original_env = os.environ.copy()
        
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "test.c")
        with open(self.temp_file, "w") as f:
            f.write("""
int     main(void)
{
    int a = 42;
    
    
    return(a);
}
""")

    def tearDown(self):
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_env)
        
        # Clean up temporary files
        if os.path.exists(self.temp_file):
            os.unlink(self.temp_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_find_executable(self):
        """Test finding an executable"""
        # Python should be findable
        python_path = find_executable("python") or find_executable("python3")
        self.assertIsNotNone(python_path, "Could not find Python executable")

    def test_find_formatter(self):
        """Test finding the formatter"""
        executable_path, module_path, method = find_formatter()
        
        # At least one of the paths should be found, or the method should be "none"
        if method != "none":
            self.assertTrue(
                executable_path is not None or module_path is not None,
                "Formatter not found but method is not 'none'"
            )
        
        print(f"Found formatter: executable={executable_path}, module={module_path}, method={method}")

    def test_environment_variable(self):
        """Test using the environment variable"""
        # Set a fake path
        os.environ["C_FORMATTER_42_PATH"] = "/fake/path"
        
        executable_path, module_path, method = find_formatter()
        
        # The method should indicate environment variable was checked
        self.assertNotEqual(method, "none", "Environment variable not checked")
        
        # Clean up
        del os.environ["C_FORMATTER_42_PATH"]

    def test_wrapper_path_flag(self):
        """Test the --wrapper-path flag"""
        # Find the wrapper script
        wrapper_script = Path(__file__).resolve().parent.parent / "wrapper" / "c_formatter_42_wrapper.py"
        
        if not wrapper_script.exists():
            self.skipTest("Wrapper script not found")
        
        # Make sure it's executable
        wrapper_script.chmod(0o755)
        
        # Run with --wrapper-path flag
        result = subprocess.run(
            [sys.executable, str(wrapper_script), "--wrapper-path"],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Check output
        self.assertEqual(result.returncode, 0, f"Command failed: {result.stderr}")
        self.assertIn("Method:", result.stdout, "Output doesn't contain 'Method:'")


if __name__ == "__main__":
    unittest.main()
