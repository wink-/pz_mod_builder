# Guide: Creating a Custom Item (Carved Branch)

This guide walks you through creating a simple mod that adds a "Carved Branch" item to Project Zomboid. We will use the existing "TreeBranch" icon but make this item a slightly better weapon than a regular stick.

## Prerequisites

- Python installed
- `pz_mod_builder` installed (`pip install .` or `poetry install`)

## Step 1: Initialize the Mod

First, create a new mod structure using the CLI tool.

```bash
pzmod init carved_branch_mod --name "Carved Branch Mod" --id "CarvedBranchMod" --authors "You"
```

This creates a folder `carved_branch_mod` with the necessary `mod.info` and `media` directories.

**Important**: You must also create a `poster.png` file in the `carved_branch_mod` directory. This is required for the mod to be valid. You can use any PNG image (e.g., 256x256 pixels).

## Step 2: Define the Item

We need to create a script file to define our new item. Project Zomboid uses `.txt` files in `media/scripts/` for this.

1.  Navigate to `carved_branch_mod/media/scripts/`.
2.  Create a new file named `carved_branch.txt`.

Open `carved_branch.txt` and add the following content:

```lua
module CarvedBranchMod {

    item CarvedBranch
    {
        Type = Weapon,
        DisplayName = Carved Branch,
        Icon = TreeBranch,
        Weight = 1.0,
        
        /* Weapon Stats - Slightly better than a normal branch */
        MinDamage = 0.3,
        MaxDamage = 0.6,
        PushBackMod = 0.3,
        DoorDamage = 1,
        TreeDamage = 0,
        KnockBackOnNoDeath = TRUE,
        SwingAnim = Bat,
        WeaponSprite = TreeBranch,
        IdleAnim = Idle_Weapon_Light,
        RunAnim = Run_Weapon_Light,
        TwoHandWeapon = FALSE,
        ConditionMax = 5,
        ConditionLowerChanceOneIn = 5,
        HitChance = 10,
        CritDmgMultiplier = 2,
    }

}
```

**Explanation:**
-   `module CarvedBranchMod`: Namespaces your items to avoid conflicts.
-   `Icon = TreeBranch`: Uses the built-in icon for a tree branch.
-   `WeaponSprite = TreeBranch`: Uses the built-in 3D model for a tree branch.
-   `MinDamage`/`MaxDamage`: We set these slightly higher than a default branch (which is very weak).

## Step 3: Create a Recipe

Now we need a way to get this item. Let's add a recipe to carve a regular Tree Branch using a Knife.

Append this to the same `carved_branch.txt` file (inside the `module` block, or after the item):

```lua
    recipe Carve Branch
    {
        Keep KitchenKnife/HuntingKnife/StoneKnife,
        TreeBranch,
        Result:CarvedBranch,
        Time:50.0,
        Category:Survivalist,
    }
```

**Explanation:**
-   `Keep ...`: Specifies that the knife is not consumed.
-   `TreeBranch`: The input item (consumed).
-   `Result:CarvedBranch`: What you get.

## Step 4: Validate the Mod

Run the validation tool to ensure everything is set up correctly.

```bash
pzmod validate carved_branch_mod
```

If everything is correct, you should see no errors.

## Step 5: Build and Install

Build the mod into a ZIP file:

```bash
pzmod build carved_branch_mod
```

To test it, extract the contents of the ZIP file into your Project Zomboid mods folder (usually `C:\Users\<User>\Zomboid\mods\`).

## Summary

You have created a mod that:
1.  Defines a new weapon `CarvedBranch`.
2.  Uses existing game assets (Icon/Model).
3.  Adds a recipe to craft it.
