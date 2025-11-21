# Examples

This directory contains example scripts demonstrating how to use pz_mod_builder.

## create_mod.py

Creates a new mod from scratch using the Python API.

```bash
python examples/create_mod.py
```

This will:
1. Create a new mod directory with proper structure
2. Generate a mod.info file
3. Create a sample Lua script
4. Validate the mod
5. Build a ZIP package

## validate_existing_mod.py

Validates an existing mod directory.

```bash
python examples/validate_existing_mod.py /path/to/your/mod
```

This will:
1. Load the mod from the specified directory
2. Display mod information
3. Run validation checks
4. Show statistics and file listing

## CLI Examples

### Create a new mod

```bash
pzmod init MyNewMod --name "My New Mod" --id "MyNewMod" --authors "Your Name"
```

### Validate a mod

```bash
pzmod validate MyNewMod
```

### Build a mod package

```bash
pzmod build MyNewMod -o ./releases
```

This creates `./releases/MyNewMod.zip` ready for distribution.

### Display mod info

```bash
pzmod info MyNewMod
```

### Build without creating a ZIP

```bash
pzmod build MyNewMod --no-zip -o ./mod_copies
```

This copies the mod directory to `./mod_copies/MyNewMod/` instead of creating a ZIP file.
