"""
Command-line interface for pz_mod_builder.
"""

import argparse
import sys
from pathlib import Path

import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from . import __version__
from .mod_builder import ModBuilder
from .mod_info import ModInfo
from .scaffold import Scaffolder

console = Console()

def cmd_init(args):
    """Initialize a new mod with mod.info file."""
    path = args.path
    
    # Interactive mode if arguments are missing
    if not args.name or not args.id:
        console.print(Panel.fit("Welcome to pz_mod_builder! Let's set up your mod.", title="Init"))
        
        if not path:
            path = questionary.text("Where should we create the mod?", default="./my_mod").ask()
            
        name = args.name or questionary.text("Mod Name (Display Name):", default="My Awesome Mod").ask()
        mod_id = args.id or questionary.text("Mod ID (Internal ID):", default=name.replace(" ", "")).ask()
        desc = args.description or questionary.text("Description:", default="A Project Zomboid mod").ask()
        authors = args.authors or questionary.text("Author(s):", default="Unknown").ask()
    else:
        name = args.name
        mod_id = args.id
        desc = args.description
        authors = args.authors
        if not path:
             console.print("[bold red]Error:[/bold red] Path is required when not in interactive mode.")
             return 1

    mod_path = Path(path)
    mod_path.mkdir(parents=True, exist_ok=True)
    
    mod_info = ModInfo()
    mod_info.name = name
    mod_info.id = mod_id
    mod_info.description = desc
    mod_info.authors = authors
    mod_info.version = args.version or "1.0"
    mod_info.pzversion = "b42"
    
    # Create basic structure
    (mod_path / 'media' / 'lua').mkdir(parents=True, exist_ok=True)
    (mod_path / 'media' / 'scripts').mkdir(parents=True, exist_ok=True)
    (mod_path / 'media' / 'textures').mkdir(parents=True, exist_ok=True)
    
    # Save mod.info
    mod_info_path = mod_path / 'mod.info'
    mod_info.save(str(mod_info_path))
    
    console.print(f"[green]Successfully initialized mod at:[/green] {mod_path}")
    console.print(f"  [bold]ID:[/bold] {mod_info.id}")
    console.print(f"  [bold]Name:[/bold] {mod_info.name}")


def cmd_validate(args):
    """Validate a mod directory."""
    try:
        with console.status("[bold green]Validating mod..."):
            builder = ModBuilder(args.path)
            issues = builder.validate()
        
        if issues:
            console.print("[bold red]Validation issues found:[/bold red]")
            for issue in issues:
                console.print(f"  [red]•[/red] {issue}")
            return 1
        else:
            console.print("[bold green]Mod validation passed![/bold green]")
            
            # Print mod info table
            if builder.mod_info:
                table = Table(title="Mod Information")
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="magenta")
                
                table.add_row("Name", builder.mod_info.name)
                table.add_row("ID", builder.mod_info.id)
                table.add_row("Version", builder.mod_info.version)
                table.add_row("PZ Version", builder.mod_info.pzversion)
                if builder.mod_info.authors:
                    table.add_row("Authors", builder.mod_info.authors)
                
                console.print(table)
            
            # Print statistics
            file_count = len(builder.get_file_list())
            size_bytes = builder.get_mod_size()
            size_mb = size_bytes / (1024 * 1024)
            
            console.print(Panel(f"Files: {file_count}\nSize: {size_mb:.2f} MB", title="Stats"))
            
            return 0
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return 1


def cmd_build(args):
    """Build a mod package."""
    try:
        builder = ModBuilder(args.path)
        
        # Validate first
        if not args.skip_validation:
            with console.status("[bold yellow]Validating before build..."):
                issues = builder.validate()
                
            if issues:
                console.print("[bold red]Validation issues found:[/bold red]")
                for issue in issues:
                    console.print(f"  [red]•[/red] {issue}")
                
                if not args.force:
                    if not questionary.confirm("Build anyway?").ask():
                        console.print("[yellow]Build aborted.[/yellow]")
                        return 1
                else:
                    console.print("[yellow]Continuing build despite validation issues...[/yellow]")
        
        # Build
        output = args.output or './mods_output'
        with console.status("[bold green]Building package..."):
            result = builder.build(output, zip_file=not args.no_zip)
        
        console.print("[bold green]Build successful![/bold green]")
        console.print(f"Output: {result}")
        return 0
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return 1


def cmd_info(args):
    """Display mod information."""
    try:
        mod_info_path = Path(args.path) / 'mod.info'
        if not mod_info_path.exists():
            console.print(f"[bold red]Error:[/bold red] mod.info not found at {mod_info_path}")
            return 1
        
        mod_info = ModInfo(str(mod_info_path))
        
        table = Table(title="Mod Information")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Name", mod_info.name)
        table.add_row("ID", mod_info.id)
        table.add_row("Description", mod_info.description)
        table.add_row("Version", mod_info.version)
        table.add_row("PZ Version", mod_info.pzversion)
        
        if mod_info.authors:
            table.add_row("Authors", mod_info.authors)
        if mod_info.url:
            table.add_row("URL", mod_info.url)
        if mod_info.poster:
            table.add_row("Poster", mod_info.poster)
        if mod_info.tile:
            table.add_row("Tile", mod_info.tile)
        if mod_info.require:
            table.add_row("Requirements", ', '.join(mod_info.require))
            
        console.print(table)
        return 0
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return 1

def cmd_add(args):
    """Add new content to the mod."""
    try:
        scaffolder = Scaffolder(args.path)
        
        if args.type == 'item':
            name = args.name or questionary.text("Item Name (ID):").ask()
            display = args.display_name or questionary.text("Display Name:", default=name).ask()
            item_type = args.item_type or questionary.select(
                "Item Type:",
                choices=["Normal", "Weapon", "Food", "Clothing", "Literature"]
            ).ask()
            
            result = scaffolder.add_item(name, display, item_type)
            console.print(f"[green]Created item:[/green] {result}")
            
        elif args.type == 'recipe':
            name = args.name or questionary.text("Recipe Name:").ask()
            result_item = args.result or questionary.text("Result Item:").ask()
            source_item = args.source or questionary.text("Source Item:", default="Base.Plank").ask()
            
            result = scaffolder.add_recipe(name, result_item, source_item)
            console.print(f"[green]Created recipe:[/green] {result}")
            
        return 0
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return 1

def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Python 3 tools for building Project Zomboid version b42 mods',
        prog='pzmod'
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new mod')
    init_parser.add_argument('path', nargs='?', help='Path to mod directory')
    init_parser.add_argument('--name', help='Mod name')
    init_parser.add_argument('--id', help='Mod ID')
    init_parser.add_argument('--description', help='Mod description')
    init_parser.add_argument('--authors', help='Mod authors')
    init_parser.add_argument(
        '--version', default='1.0', help='Mod version (default: 1.0)'
    )
    init_parser.set_defaults(func=cmd_init)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a mod')
    validate_parser.add_argument('path', help='Path to mod directory')
    validate_parser.set_defaults(func=cmd_validate)
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build a mod package')
    build_parser.add_argument('path', help='Path to mod directory')
    build_parser.add_argument(
        '-o', '--output', help='Output directory (default: ./mods_output)'
    )
    build_parser.add_argument(
        '--no-zip', action='store_true', help='Do not create ZIP file'
    )
    build_parser.add_argument(
        '--skip-validation', action='store_true', help='Skip validation'
    )
    build_parser.add_argument(
        '--force', action='store_true', help='Build even with validation issues'
    )
    build_parser.set_defaults(func=cmd_build)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Display mod information')
    info_parser.add_argument('path', help='Path to mod directory')
    info_parser.set_defaults(func=cmd_info)
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add content to mod')
    add_parser.add_argument('path', help='Path to mod directory')
    add_subparsers = add_parser.add_subparsers(dest='type', help='Content type')
    
    # Add Item
    add_item_parser = add_subparsers.add_parser('item', help='Add a new item')
    add_item_parser.add_argument('--name', help='Item name (ID)')
    add_item_parser.add_argument('--display-name', help='Display name')
    add_item_parser.add_argument('--item-type', help='Item type')
    
    # Add Recipe
    add_recipe_parser = add_subparsers.add_parser('recipe', help='Add a new recipe')
    add_recipe_parser.add_argument('--name', help='Recipe name')
    add_recipe_parser.add_argument('--result', help='Result item')
    add_recipe_parser.add_argument('--source', help='Source item')
    
    add_parser.set_defaults(func=cmd_add)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
