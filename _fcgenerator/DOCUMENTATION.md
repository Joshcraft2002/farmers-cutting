Very incomplete documentation, I'll fix it up at a later time (should this be a wiki instead? idk)
---
# Farmer's Cutting Generator (fcgenerator)
Generates [beet](https://mcbeet.dev/) projects for building Farmer's Cutting datapacks.

### Versioning
```x.yz```
#### Farmer's Cutting
- `x`: New mod items
- `y`: Mod changes
- `z`: Datapack patch
#### Farmer's Collection
- `x`: New Minecraft version (new mod collection)
- `y`: Mod Added/Changed
- `z`: Datapack patch

## Project Structure

```
root/
├─ .fcgenerator/
│  └─ config/
│     └─ <modid>/
│        ├─ data/
│        ├─ custom.json
│        ├─ dye.json
│        ├─ mod.json
│        └─ wood.json
├─ <modid>/
│   ├─ fabric/
│   ├─ forge/
│   └─ neoforge/
├─ fccollection/
│   ├─ fabric/
│   ├─ forge/
│   └─ neoforge/
└─ fcgenerator.py
```

### Directory & File Overview

| Path                                      | Description                               |
| ----------------------------------------- | ----------------------------------------- |
| `.fcgenerator/config/<modid>/`            | Configuration files for a mod             |
| `.fcgenerator/config/<modid>/custom.json` | Custom cutting recipes                    |
| `.fcgenerator/config/<modid>/dye.json`    | Dye cutting recipes                       |
| `.fcgenerator/config/<modid>/mod.json`    | Datapack configuration                    |
| `.fcgenerator/config/<modid>/wood.json`   | Wood cutting recipes                      |
| `.fcgenerator/config/generator.json`      | Generator Configuration                   |
| `<modid>/fabric/`                         | Fabric beet project for this mod          |
| `<modid>/forge/`                          | Forge beet project for this mod           |
| `<modid>/neoforge/`                       | NeoForge project for this mod             |
| `fccollection/fabric/`                    | Collection of all Fabric projects         |
| `fccollection/forge/`                     | Collection of all Forge projects          |
| `fccollection/neoforge/`                  | Collection of all NeoForge projects       |
| `fcgenerator.py`                          | Main generator script                     |

---

## Usage

1. **Configure**  
   Place configuration files for each mod in `.fcgenerator/config/<modid>/`.  
   Example files: `custom.json`, `dye.json`, `mod.json`.

2. **Generate**  
   Run `fcgenerator.py` to generate beet projects for each mod and loader.

3. **Build**  
   Use [beet](https://mcbeet.dev/) to build the generated projects into datapacks.

---

## Configuration

A template for configuration files can be found at `.fcgenerator/config/_template/`

### `mod.json`
Defines general metadata and settings for the mod to generate for.

```json
{
  "name": "Example Mod",
  "namespace": "examplemod",
  "id_suffix": "em",
  "data_pack_version": "1.0",
  "pack_format": 48,
  "platforms": ["fabric", "neoforge"],
  "enable_logging": true
}
```

| Field               | Type     | Description 
| ------------------- | -------- | ----------- 
| `name`              | string   | Mod name 
| `namespace`         | string   | Mod ID 
| `id_suffix`         | string   | Short identifier for output folders/files 
| `data_pack_version` | string   | Version string for the data pack 
| `pack_format`       | int      | Minecraft data pack format number 
| `platforms`         | string[] | List of modloaders to generate for 
| `enable_logging`    | bool     | If true, logs file generation. 

`platforms` allowed values: `fabric`, `forge`, `neoforge`

### `wood.json`
Specifies which woods and recipe types to generate, and allows for overrides.

```json
{
  "wood_recipes": {
    "woods": ["example_oak", "interesting_pine", "another_mangrove"],
    "types": ["door", "hanging_sign", "sign", "trapdoor", "log", "wood"]
  },
  "overrides": [
    {
      "type": "replace_recipe_types",
      "wood": "interesting_pine",
      "recipe_types": ["log", "wood"]
    },
    {
      "type": "replace_single_recipe",
      "wood": "interesting_pine",
      "recipe_type": "log",
      "ingredient": "examplemod:interesting_pine_log",
      "result": "examplemod:stripped_interesting_pine_log",
      "side_product": "farmersdelight:tree_bark"
    }
  ]
}
```
- `wood_recipes.woods`: List of wood types to generate recipes for.
- `wood_recipes.types`: List of recipe types to generate for each wood.
- `overrides`: List of override objects. Any number of these objects can be present.
  - `type`: type of override
    - `replace_recipe_types`: Replace the recipe types for a specific wood.
      - `wood`: wood 
    - `replace_single_recipe`: Replace a single recipe for a wood and type, optionally specifying `ingredient`, `result`, and `side_product`.

---

### `dye.json`
Defines dye recipes.

```json
{
  "recipes": [
    {"input": "flower", "color": "red", "count": 2},
    {"input": "another_flower", "color": "purple", "count": 2}
  ]
}
```
- `input`: Item or tag (prefix with `#` for tag) to use as ingredient.
- `color`: Minecraft dye color.
- `count`: Number of dye items produced.

---

### `custom.json`
Defines custom cutting recipes.

```json
{
  "recipes": [
    {
      "ingredient": "examplemod:shiny_block",
      "result": "examplemod:shiny_chunk",
      "count": 4,
      "tool": "pickaxe",
      "filename": "shiny_block"
    },
    {
      "ingredient": "examplemod:unique_wood",
      "result": "examplemod:stripped_unique_wood",
      "count": 1,
      "side_product": "examplemod:unique_item",
      "tool": "axe_strip",
      "filename": "shiny_block"
    }
  ]
}
```
- `ingredient`: Item or tag (prefix with `#` for tag) to use as ingredient.
- `result`: Output item.
- `count`: Number of result items.
- `side_product`: (Optional) Additional output item.
- `tool`: Tool required (`axe`, `axe_strip`, `pickaxe`, `knife`).
- `filename`: Name for the generated recipe file.