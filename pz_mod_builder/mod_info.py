"""
Module for handling Project Zomboid mod.info files (b42 format).
"""

import re
from typing import Dict, Optional, List


class ModInfo:
    """
    Parser and handler for Project Zomboid mod.info files.
    
    The mod.info file contains metadata about a mod including name, ID,
    description, and other attributes specific to PZ b42.
    """
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize ModInfo.
        
        Args:
            file_path: Optional path to existing mod.info file to parse
        """
        self.name: str = ""
        self.id: str = ""
        self.description: str = ""
        self.poster: str = ""
        self.tile: str = ""
        self.authors: str = ""
        self.version: str = "1.0"
        self.url: str = ""
        self.modversion: str = ""
        self.pzversion: str = "b42"
        self.require: List[str] = []
        
        if file_path:
            self.load(file_path)
    
    def load(self, file_path: str) -> None:
        """
        Load and parse a mod.info file.
        
        Args:
            file_path: Path to the mod.info file
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._parse_content(content)
    
    def _parse_content(self, content: str) -> None:
        """
        Parse the content of a mod.info file.
        
        Args:
            content: String content of mod.info file
        """
        # Parse key=value pairs
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                if key == 'name':
                    self.name = value
                elif key == 'id':
                    self.id = value
                elif key == 'description':
                    self.description = value
                elif key == 'poster':
                    self.poster = value
                elif key == 'tile':
                    self.tile = value
                elif key == 'authors':
                    self.authors = value
                elif key == 'version':
                    self.version = value
                elif key == 'url':
                    self.url = value
                elif key == 'modversion':
                    self.modversion = value
                elif key == 'pzversion':
                    self.pzversion = value
                elif key == 'require':
                    # Handle comma-separated requirements
                    self.require = [r.strip() for r in value.split(',') if r.strip()]
    
    def save(self, file_path: str) -> None:
        """
        Save the mod info to a file.
        
        Args:
            file_path: Path where to save the mod.info file
        """
        content = self.to_string()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def to_string(self) -> str:
        """
        Convert mod info to string format.
        
        Returns:
            String representation in mod.info format
        """
        lines = []
        
        if self.name:
            lines.append(f"name={self.name}")
        if self.id:
            lines.append(f"id={self.id}")
        if self.description:
            lines.append(f"description={self.description}")
        if self.poster:
            lines.append(f"poster={self.poster}")
        if self.tile:
            lines.append(f"tile={self.tile}")
        if self.authors:
            lines.append(f"authors={self.authors}")
        if self.version:
            lines.append(f"version={self.version}")
        if self.url:
            lines.append(f"url={self.url}")
        if self.modversion:
            lines.append(f"modversion={self.modversion}")
        if self.pzversion:
            lines.append(f"pzversion={self.pzversion}")
        if self.require:
            lines.append(f"require={','.join(self.require)}")
        
        return '\n'.join(lines) + '\n'
    
    def validate(self) -> List[str]:
        """
        Validate the mod info and return any errors.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if not self.name:
            errors.append("Mod name is required")
        if not self.id:
            errors.append("Mod ID is required")
        if self.id and not re.match(r'^[A-Za-z0-9_]+$', self.id):
            errors.append("Mod ID must contain only letters, numbers, and underscores")
        if not self.description:
            errors.append("Mod description is required")
        
        return errors
    
    def __repr__(self) -> str:
        return f"ModInfo(name={self.name!r}, id={self.id!r}, version={self.version!r})"
