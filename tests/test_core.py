import os
import tempfile
from pathlib import Path
import unittest
from promptpack_for_code.core import process_directory, generate_tree

class TestPromptPackForCode(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        self.root_dir = Path(self.test_dir)
        
        # Create test file structure
        self.create_test_files()
        
    def create_test_files(self):
        # Create directories
        src_dir = self.root_dir / "src"
        src_dir.mkdir()
        utils_dir = src_dir / "utils"
        utils_dir.mkdir()
        
        # Create some test files
        (src_dir / "main.py").write_text("def main():\n    print('Hello')\n")
        (utils_dir / "helper.py").write_text("def helper():\n    return True\n")
        
        # Create file to ignore
        (src_dir / "ignored.pyc").write_text("should not appear")
        
    def tearDown(self):
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(self.test_dir)
        
    def test_generate_tree(self):
        tree = generate_tree(self.root_dir)
        self.assertIn("src", tree)
        self.assertIn("utils", tree)
        self.assertIn("main.py", tree)
        self.assertIn("helper.py", tree)
        self.assertNotIn("ignored.pyc", tree)
        
    def test_process_directory(self):
        output_file = self.root_dir / "output.txt"
        process_directory(
            str(self.root_dir / "src"),
            str(self.root_dir),
            str(output_file)
        )
        
        # Check if output file exists
        self.assertTrue(output_file.exists())
        
        # Read the output file
        content = output_file.read_text()
        
        # Check if tree structure is included
        self.assertIn("Project Directory Structure:", content)
        
        # Check if file contents are included
        self.assertIn("File Contents from Selected Directory:", content)
        self.assertIn("def main():", content)
        self.assertIn("def helper():", content)
        
        # Check if ignored files are excluded
        self.assertNotIn("should not appear", content)

    def test_process_directory_with_custom_ignore(self):
        output_file = self.root_dir / "output.txt"
        process_directory(
            str(self.root_dir / "src"),
            str(self.root_dir),
            str(output_file),
            ignore_patterns=["*.py"]  # Ignore all Python files
        )
        
        content = output_file.read_text()
        self.assertNotIn("def main():", content)
        self.assertNotIn("def helper():", content)

if __name__ == '__main__':
    unittest.main()
