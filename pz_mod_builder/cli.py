"""
Command-line interface for pz_mod_builder.
"""

import argparse
import sys
from pathlib import Path

from . import __version__
from .mod_info import ModInfo
from .mod_builder import ModBuilder


def cmd_init(args):
    """Initialize a new mod with mod.info file."""
    mod_path = Path(args.path)
    mod_path.mkdir(parents=True, exist_ok=True)
    
    mod_info = ModInfo()
    mod_info.name = args.name or mod_path.name
    mod_info.id = args.id or mod_path.name
    mod_info.description = args.description or f"A Project Zomboid mod: {mod_info.name}"
    mod_info.authors = args.authors or ""
    mod_info.version = args.version or "1.0"
    mod_info.pzversion = "b42"
    
    # Create basic structure
    (mod_path / 'media' / 'lua').mkdir(parents=True, exist_ok=True)
    (mod_path / 'media' / 'scripts').mkdir(parents=True, exist_ok=True)
    (mod_path / 'media' / 'textures').mkdir(parents=True, exist_ok=True)
    
    # Save mod.info
    mod_info_path = mod_path / 'mod.info'
    mod_info.save(str(mod_info_path))
    
    print(f"Initialized mod at: {mod_path}")
    print(f"Mod ID: {mod_info.id}")
    print(f"Mod Name: {mod_info.name}")


def cmd_validate(args):
    """Validate a mod directory."""
    try:
        builder = ModBuilder(args.path)
        issues = builder.validate()
        
        if issues:
            print("Validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return 1
        else:
            print("Mod validation passed!")
            
            # Print mod info
            if builder.mod_info:
                print(f"\nMod: {builder.mod_info.name} (ID: {builder.mod_info.id})")
                print(f"Version: {builder.mod_info.version}")
                print(f"PZ Version: {builder.mod_info.pzversion}")
                if builder.mod_info.authors:
                    print(f"Authors: {builder.mod_info.authors}")
            
            # Print statistics
            file_count = len(builder.get_file_list())
            size_bytes = builder.get_mod_size()
            size_mb = size_bytes / (1024 * 1024)
            print(f"\nFiles: {file_count}")
            print(f"Size: {size_mb:.2f} MB")
            
            return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_build(args):
    """Build a mod package."""
    try:
        builder = ModBuilder(args.path)
        
        # Validate first
        if not args.skip_validation:
            issues = builder.validate()
            if issues:
                print("Validation issues found:")
                for issue in issues:
                    print(f"  - {issue}")
                if not args.force:
                    print("\nBuild aborted. Use --force to build anyway.")
                    return 1
                else:
                    print("\nContinuing build despite validation issues...")
        
        # Build
        output = args.output or './mods_output'
        result = builder.build(output, zip_file=not args.no_zip)
        
        print(f"Build successful!")
        print(f"Output: {result}")
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_info(args):
    """Display mod information."""
    try:
        mod_info_path = Path(args.path) / 'mod.info'
        if not mod_info_path.exists():
            print(f"Error: mod.info not found at {mod_info_path}", file=sys.stderr)
            return 1
        
        mod_info = ModInfo(str(mod_info_path))
        
        print("Mod Information:")
        print(f"  Name: {mod_info.name}")
        print(f"  ID: {mod_info.id}")
        print(f"  Description: {mod_info.description}")
        print(f"  Version: {mod_info.version}")
        print(f"  PZ Version: {mod_info.pzversion}")
        
        if mod_info.authors:
            print(f"  Authors: {mod_info.authors}")
        if mod_info.url:
            print(f"  URL: {mod_info.url}")
        if mod_info.poster:
            print(f"  Poster: {mod_info.poster}")
        if mod_info.tile:
            print(f"  Tile: {mod_info.tile}")
        if mod_info.require:
            print(f"  Requirements: {', '.join(mod_info.require)}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Python 3 tools for building Project Zomboid version b42 mods',
        prog='pzmod'
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new mod')
    init_parser.add_argument('path', help='Path to mod directory')
    init_parser.add_argument('--name', help='Mod name')
    init_parser.add_argument('--id', help='Mod ID')
    init_parser.add_argument('--description', help='Mod description')
    init_parser.add_argument('--authors', help='Mod authors')
    init_parser.add_argument('--version', default='1.0', help='Mod version (default: 1.0)')
    init_parser.set_defaults(func=cmd_init)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a mod')
    validate_parser.add_argument('path', help='Path to mod directory')
    validate_parser.set_defaults(func=cmd_validate)
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build a mod package')
    build_parser.add_argument('path', help='Path to mod directory')
    build_parser.add_argument('-o', '--output', help='Output directory (default: ./mods_output)')
    build_parser.add_argument('--no-zip', action='store_true', help='Do not create ZIP file')
    build_parser.add_argument('--skip-validation', action='store_true', help='Skip validation')
    build_parser.add_argument('--force', action='store_true', help='Build even with validation issues')
    build_parser.set_defaults(func=cmd_build)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Display mod information')
    info_parser.add_argument('path', help='Path to mod directory')
    info_parser.set_defaults(func=cmd_info)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
