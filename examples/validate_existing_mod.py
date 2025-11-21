#!/usr/bin/env python3
"""
Example: Validating an existing Project Zomboid b42 mod.
"""

import sys
from pz_mod_builder import ModBuilder


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_existing_mod.py <mod_directory>")
        sys.exit(1)
    
    mod_path = sys.argv[1]
    
    try:
        # Load the mod
        print(f"Loading mod from: {mod_path}")
        builder = ModBuilder(mod_path)
        
        # Display mod information
        if builder.mod_info:
            print("\nMod Information:")
            print(f"  Name: {builder.mod_info.name}")
            print(f"  ID: {builder.mod_info.id}")
            print(f"  Version: {builder.mod_info.version}")
            print(f"  PZ Version: {builder.mod_info.pzversion}")
            if builder.mod_info.authors:
                print(f"  Authors: {builder.mod_info.authors}")
        
        # Validate
        print("\nValidating mod...")
        issues = builder.validate()
        
        if issues:
            print("\nValidation issues found:")
            for issue in issues:
                print(f"  ❌ {issue}")
            sys.exit(1)
        else:
            print("✓ Mod validation passed!")
        
        # Display statistics
        print("\nMod Statistics:")
        files = builder.get_file_list()
        print(f"  Total files: {len(files)}")
        print(f"  Total size: {builder.get_mod_size() / 1024:.2f} KB")
        
        # List all files
        print("\nFiles in mod:")
        for file in files:
            print(f"  - {file}")
        
    except FileNotFoundError:
        print(f"Error: Mod directory not found: {mod_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
