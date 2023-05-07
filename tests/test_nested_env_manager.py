import os
import tempfile
import unittest
from nested_env_manager.nested_env_manager import NestedEnvManager

class TestNestedEnvManager(unittest.TestCase):
    def setUp(self):
        self.nem = NestedEnvManager()
        self.main_env_requirements = ["numpy"]
        self.main_env_path = tempfile.mkdtemp()

        self.sub_env_requirements = ["pandas"]
        self.sub_env_path = tempfile.mkdtemp()

        self.nem.create_main_env(self.main_env_requirements, self.main_env_path)

    def test_create_main_env(self):
        self.assertTrue(os.path.exists(self.main_env_path))
        self.assertTrue(os.path.exists(os.path.join(self.main_env_path, "virtual_root")))

    def test_create_sub_env(self):
        self.nem.create_sub_env(self.sub_env_requirements, self.sub_env_path)
        self.assertTrue(os.path.exists(self.sub_env_path))

    def test_execute_script_in_main_env(self):
        test_script = "test_main_env_script.py"
        with open(os.path.join(self.nem.virtual_root, test_script), "w") as f:
            f.write("import numpy\nprint('Main env script executed')")

        self.nem.execute_script_in_main_env(test_script)

    def test_execute_script_in_sub_env(self):
        self.nem.create_sub_env(self.sub_env_requirements, self.sub_env_path)

        test_script = "test_sub_env_script.py"
        with open(os.path.join(self.nem.virtual_root, test_script), "w") as f:
            f.write("import pandas\nprint('Sub env script executed')")

        self.nem.execute_script_in_sub_env(self.sub_env_path, test_script)

if __name__ == "__main__":
    unittest.main()
