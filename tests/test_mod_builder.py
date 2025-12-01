import shutil
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from pz_mod_builder.mod_builder import ModBuilder


class TestModBuilder(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.mod_path = Path(self.test_dir) / "test_mod"
        self.mod_path.mkdir()
        
        # Create valid mod.info
        self.mod_info_path = self.mod_path / "mod.info"
        with open(self.mod_info_path, "w") as f:
            f.write(
                "name=Test Mod\n"
                "id=TestMod\n"
                "description=Test Description\n"
                "poster=poster.png\n"
                "tile=tile.png\n"
            )
            
    def tearDown(self):
        shutil.rmtree(self.test_dir)
        
    def test_validate_missing_images(self):
        builder = ModBuilder(str(self.mod_path))
        issues = builder.validate()
        self.assertTrue(any("Poster image not found" in i for i in issues))
        self.assertTrue(any("Tile image not found" in i for i in issues))
        
    def test_validate_valid_images(self):
        # Create valid images
        img = Image.new('RGB', (60, 30), color = 'red')
        img.save(self.mod_path / "poster.png")
        img.save(self.mod_path / "tile.png")
        
        builder = ModBuilder(str(self.mod_path))
        issues = builder.validate()
        # Filter out "Missing mod.info file" if it appears
        # Check for other issues like "Unusual file extension"
        # but here we only have .png which is valid.
        self.assertEqual(len(issues), 0, f"Found issues: {issues}")
        
    def test_validate_invalid_images(self):
        # Create invalid images (text files disguised as png)
        with open(self.mod_path / "poster.png", "w") as f:
            f.write("not an image")
        with open(self.mod_path / "tile.png", "w") as f:
            f.write("not an image")
            
        builder = ModBuilder(str(self.mod_path))
        issues = builder.validate()
        self.assertTrue(any("Invalid poster image" in i for i in issues))
        self.assertTrue(any("Invalid tile image" in i for i in issues))

if __name__ == '__main__':
    unittest.main()
