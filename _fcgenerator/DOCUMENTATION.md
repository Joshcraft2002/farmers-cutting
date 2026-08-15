Very incomplete documentation, I'll fix it up at a later time (should this be a wiki instead? idk)
---
# Farmer's Cutting Generator (fcgenerator)
Generates [beet](https://mcbeet.dev/) projects for building Farmer's Cutting datapacks.

### Versioning
#### Farmer's Cutting
```x.yz```
- `x`: New mod items
- `y`: Mod changes
- `z`: Datapack patch
#### Farmer's Cutting Collection
```x.yz```
- `x`: New Minecraft version (new mod collection)
- `y`: Mod added/changed
- `z`: Datapack patch
#### FCGenerator
```w-0.x.yz```
- `w`: Minecraft version
- `x`: Major (breaking) changes
  - any changes where existing config files cannot be reused are considered major
- `y`: Minor changes
- `z`: Patches

## Project Structure

```
root/
├─ .fcgenerator/
│  └─ config/
│     └─ <modid>/
│        ├─ extras/
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
| `_fcgenerator/config/<modid>/extras/`     | Holds raw datapack files not covered by the generator   |
| `<directory>`                             | Directory description (to be rewritten)   |

---

## Usage

1. Place configuration files for each mod in `.fcgenerator/config/<modid>/`. 
2. Run `fcgenerator.py` to generate beet projects for each mod and loader.
3. Use [beet](https://mcbeet.dev/) to build the generated projects into datapacks. Directory names are the mod ids specified in each config.

---

## Configuration

A template for configuration files can be found at [config/_template/](config/_template/)

### `mod.json`
Defines general metadata and settings of the mod to generate for.

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
- `tool`: Tool required (`axe`, `axe_strip`, `pickaxe`, `knife`, `shear`).
- `filename`: Name for the generated recipe file.