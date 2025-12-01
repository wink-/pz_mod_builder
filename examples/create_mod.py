#!/usr/bin/env python3
"""
Example: Creating a new Project Zomboid b42 mod using the Python API.
"""

import os

from pz_mod_builder import ModBuilder, ModInfo


def main():
    # Create mod directory
    mod_dir = "my_example_mod"
    os.makedirs(mod_dir, exist_ok=True)
    os.makedirs(f"{mod_dir}/media/lua/client", exist_ok=True)
    
    # Create mod.info
    print("Creating mod.info...")
    mod_info = ModInfo()
    mod_info.name = "Example Mod"
    mod_info.id = "ExampleMod"
    mod_info.description = "An example mod created with pz_mod_builder"
    mod_info.authors = "Your Name"
    mod_info.version = "1.0"
    mod_info.pzversion = "b42"
    mod_info.url = "https://github.com/yourname/example-mod"
    
    # Save mod.info
    mod_info.save(f"{mod_dir}/mod.info")
    print(f"Created mod.info for {mod_info.name}")
    
    # Create a simple Lua script
    print("\nCreating Lua script...")
    lua_content = """-- Example client-side Lua script
-- This runs when the mod loads on the client

Events.OnGameStart.Add(function()
    print("Example Mod loaded successfully!")
    print("Welcome to Project Zomboid b42!")
end)
"""
    
    with open(f"{mod_dir}/media/lua/client/example.lua", 'w') as f:
        f.write(lua_content)
    print("Created example.lua")
    
    # Validate the mod
    print("\nValidating mod...")
    builder = ModBuilder(mod_dir)
    issues = builder.validate()
    
    if issues:
        print("Validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Mod is valid!")
    
    # Display mod info
    print("\nMod statistics:")
    print(f"  Files: {len(builder.get_file_list())}")
    print(f"  Size: {builder.get_mod_size()} bytes")
    
    # Build the mod
    print("\nBuilding mod package...")
    output = builder.build("./output", zip_file=True)
    print(f"Mod built successfully: {output}")


if __name__ == "__main__":
    main()
