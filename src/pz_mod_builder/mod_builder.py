"""
Module for building and packaging Project Zomboid b42 mods.
"""

import shutil
import zipfile
from pathlib import Path
from typing import List, Optional

from PIL import Image, UnidentifiedImageError

from .mod_info import ModInfo


class ModBuilder:
    """
    Builder for Project Zomboid mod packages.
    
    Handles validation, packaging, and building of mod directories into
    distributable formats for PZ b42.
    """
    
    # Standard mod directory structure for PZ b42
    VALID_DIRECTORIES = {
        'media',
        'media/lua',
        'media/scripts',
        'media/textures',
        'media/ui',
        'media/sound',
        'media/models',
        'media/clothing',
        'media/maps',
    }
    
    # Valid file extensions for PZ b42 mods
    VALID_EXTENSIONS = {
        '.lua',
        '.txt',
        '.png',
        '.ogg',
        '.wav',
        '.xml',
        '.json',
        '.fbx',
        '.bin',
        '.tiles',
        '.tmx',
        '.tsx',
    }
    
    def __init__(self, mod_path: str):
        """
        Initialize the ModBuilder.
        
        Args:
            mod_path: Path to the mod directory
        """
        self.mod_path = Path(mod_path)
        self.mod_info: Optional[ModInfo] = None
        
        if not self.mod_path.exists():
            raise FileNotFoundError(f"Mod directory not found: {mod_path}")
        
        # Try to load mod.info if it exists
        mod_info_path = self.mod_path / 'mod.info'
        if mod_info_path.exists():
            self.mod_info = ModInfo(str(mod_info_path))
    
    def validate(self) -> List[str]:
        """
        Validate the mod structure and contents.
        
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        # Check for mod.info
        mod_info_path = self.mod_path / 'mod.info'
        if not mod_info_path.exists():
            issues.append("Missing mod.info file")
        elif self.mod_info:
            # Validate mod.info content
            info_errors = self.mod_info.validate()
            issues.extend(info_errors)
        
        # Check for poster image if specified
        if self.mod_info and self.mod_info.poster:
            poster_path = self.mod_path / self.mod_info.poster
            if not poster_path.exists():
                issues.append(f"Poster image not found: {self.mod_info.poster}")
            else:
                try:
                    with Image.open(poster_path) as img:
                        img.verify()
                except (IOError, UnidentifiedImageError):
                    issues.append(f"Invalid poster image: {self.mod_info.poster}")
        
        # Check for tile image if specified
        if self.mod_info and self.mod_info.tile:
            tile_path = self.mod_path / self.mod_info.tile
            if not tile_path.exists():
                issues.append(f"Tile image not found: {self.mod_info.tile}")
            else:
                try:
                    with Image.open(tile_path) as img:
                        img.verify()
                except (IOError, UnidentifiedImageError):
                    issues.append(f"Invalid tile image: {self.mod_info.tile}")
        
        # Validate file extensions
        for file_path in self.mod_path.rglob('*'):
            if file_path.is_file() and file_path.name != 'mod.info':
                ext = file_path.suffix.lower()
                if ext and ext not in self.VALID_EXTENSIONS:
                    rel_path = file_path.relative_to(self.mod_path)
                    issues.append(f"Unusual file extension: {rel_path}")
        
        return issues
    
    def build(self, output_dir: str, zip_file: bool = True) -> str:
        """
        Build the mod package.
        
        Args:
            output_dir: Directory where to output the built mod
            zip_file: Whether to create a ZIP file (default: True)
        
        Returns:
            Path to the built mod (directory or zip file)
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Determine mod name for output
        if self.mod_info and self.mod_info.id:
            mod_name = self.mod_info.id
        else:
            mod_name = self.mod_path.name
        
        if zip_file:
            # Create ZIP file
            zip_path = output_path / f"{mod_name}.zip"
            self._create_zip(zip_path)
            return str(zip_path)
        else:
            # Copy to output directory
            mod_output = output_path / mod_name
            if mod_output.exists():
                shutil.rmtree(mod_output)
            shutil.copytree(self.mod_path, mod_output)
            return str(mod_output)
    
    def _create_zip(self, zip_path: Path) -> None:
        """
        Create a ZIP file of the mod.
        
        Args:
            zip_path: Path where to create the ZIP file
        """
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.mod_path.rglob('*'):
                if file_path.is_file():
                    # Skip hidden files and build artifacts
                    if file_path.name.startswith('.'):
                        continue
                    
                    arcname = file_path.relative_to(self.mod_path)
                    zipf.write(file_path, arcname)
    
    def get_file_list(self) -> List[str]:
        """
        Get a list of all files in the mod.
        
        Returns:
            List of relative file paths
        """
        files = []
        for file_path in self.mod_path.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.mod_path)
                files.append(str(rel_path))
        return sorted(files)
    
    def get_mod_size(self) -> int:
        """
        Get the total size of the mod in bytes.
        
        Returns:
            Total size in bytes
        """
        total_size = 0
        for file_path in self.mod_path.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
