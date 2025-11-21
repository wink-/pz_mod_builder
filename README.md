# pz_mod_builder

Python 3 tools for building Project Zomboid version b42 mods.

## Features

- **mod.info Parser**: Read, write, and validate Project Zomboid mod.info files
- **Mod Builder**: Package and build mods with automatic validation
- **CLI Interface**: Easy-to-use command-line tools for mod management
- **File Validation**: Ensure your mod follows PZ b42 standards
- **ZIP Packaging**: Create distributable mod packages

## Installation

Install from source:

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

## Quick Start

### Initialize a New Mod

```bash
pzmod init my_awesome_mod --name "My Awesome Mod" --id "MyAwesomeMod" --authors "Your Name"
```

This creates a mod directory with the standard structure:
- `mod.info` - Mod metadata
- `media/lua/` - Lua scripts
- `media/scripts/` - Game scripts
- `media/textures/` - Textures and images

### Validate a Mod

```bash
pzmod validate my_awesome_mod
```

### Build a Mod Package

```bash
pzmod build my_awesome_mod -o ./output
```

This creates a ZIP file ready for distribution.

### Display Mod Information

```bash
pzmod info my_awesome_mod
```

## Python API

You can also use pz_mod_builder as a Python library:

```python
from pz_mod_builder import ModInfo, ModBuilder

# Create mod metadata
mod_info = ModInfo()
mod_info.name = "My Mod"
mod_info.id = "MyMod"
mod_info.description = "A great mod"
mod_info.version = "1.0"
mod_info.pzversion = "b42"
mod_info.save("my_mod/mod.info")

# Build a mod
builder = ModBuilder("my_mod")
issues = builder.validate()
if not issues:
    builder.build("./output", zip_file=True)
```

## mod.info Format

The `mod.info` file contains metadata about your mod:

```
name=My Awesome Mod
id=MyAwesomeMod
description=This mod adds awesome features to Project Zomboid
poster=poster.png
tile=tile.png
authors=Your Name
version=1.0
url=https://github.com/yourname/your-mod
pzversion=b42
```

## CLI Commands

### `pzmod init <path>`

Initialize a new mod directory with basic structure.

Options:
- `--name` - Mod display name
- `--id` - Mod ID (used for internal identification)
- `--description` - Mod description
- `--authors` - Mod authors
- `--version` - Mod version (default: 1.0)

### `pzmod validate <path>`

Validate a mod directory structure and metadata.

### `pzmod build <path>`

Build and package a mod.

Options:
- `-o, --output` - Output directory (default: ./mods_output)
- `--no-zip` - Copy files instead of creating a ZIP
- `--skip-validation` - Skip validation step
- `--force` - Build even with validation issues

### `pzmod info <path>`

Display mod information from mod.info file.

## Project Structure

```
my_mod/
├── mod.info              # Mod metadata (required)
├── poster.png            # Mod poster image (optional)
├── tile.png              # Mod tile image (optional)
└── media/
    ├── lua/              # Lua scripts
    │   └── client/
    │   └── server/
    │   └── shared/
    ├── scripts/          # Game definition scripts
    ├── textures/         # Images and textures
    ├── ui/               # UI elements
    ├── sound/            # Audio files
    └── maps/             # Custom maps
```

## Requirements

- Python 3.7 or higher

## License

MIT
