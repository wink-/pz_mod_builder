"""
Module for scaffolding new mod content.
"""

from pathlib import Path
from typing import Optional

class Scaffolder:
    """Generates boilerplate code for mod content."""
    
    def __init__(self, mod_path: str):
        self.mod_path = Path(mod_path)
        
    def add_item(self, name: str, display_name: Optional[str] = None, item_type: str = "Normal") -> str:
        """
        Add a new item definition.
        
        Args:
            name: Internal item name (ID)
            display_name: Display name (defaults to name)
            item_type: Item type (Normal, Weapon, Food, etc.)
            
        Returns:
            Path to the created file
        """
        display_name = display_name or name
        filename = name.lower().replace(" ", "_")
        
        content = f"""module MyMod {{

    item {name}
    {{
        Type = {item_type},
        DisplayName = {display_name},
        Icon = Question,
        Weight = 1.0,
    }}

}}
"""
        
        scripts_dir = self.mod_path / 'media' / 'scripts'
        scripts_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = scripts_dir / f"{filename}.txt"
        
        # Don't overwrite existing files
        if file_path.exists():
            raise FileExistsError(f"File already exists: {file_path}")
            
        with open(file_path, 'w') as f:
            f.write(content)
            
        return str(file_path)

    def add_recipe(self, name: str, result: str, source: str = "Base.Plank") -> str:
        """
        Add a new recipe definition.
        
        Args:
            name: Recipe name
            result: Result item
            source: Source item
            
        Returns:
            Path to the created file
        """
        filename = name.lower().replace(" ", "_") + "_recipe"
        
        content = f"""module MyMod {{

    recipe {name}
    {{
        {source},
        Result:{result},
        Time:50.0,
        Category:Survivalist,
    }}

}}
"""
        
        scripts_dir = self.mod_path / 'media' / 'scripts'
        scripts_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = scripts_dir / f"{filename}.txt"
        
        if file_path.exists():
            raise FileExistsError(f"File already exists: {file_path}")
            
        with open(file_path, 'w') as f:
            f.write(content)
            
        return str(file_path)
