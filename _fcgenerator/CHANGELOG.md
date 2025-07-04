# 0.2.1 (2025-06-06)
- Further customization for the collection data pack in `generator.json` config
  - Also added option not to generate a collection data pack
- added `extras` example in the [template](config/_template) config

# 0.2.0 (2025-06-06)

## Added
- Now generates a Farmer's Cutting: Collection data pack (`fccollection`), a combination of all Farmer's Cutting recipes specified in the generator config
- More custom recipe tools supported: `shears` (`c:tools/shears`), `hoe` (`hoe_dig`), `shovel` (`shovel_dig`)
- [DOCUMENTATION.md](DOCUMENTATION.md) for some extra generator information

## Changed
- `fcgenerator` directory renamed to `_fcgenerator`
  - config moved to `_fcgenerator/config`
- Generator script split up into additional modules in `_fcgenerator/generator`
- Output project files are now placed in `<mod_id>/<platform>` directories, even if only one platform is supported (previously, the case would be that files were output directly to `<mod_id>`)
### Config Format
- Mod config files are now split into a required `mod.json` file and optional `wood.json`, `dyes.json`, and `custom.json` files, inside a folder with the Mod ID as the name
- Added an `extras` folder for manually creating datapack files that cannot be handled by the generator
- `namespace` and `name` fields have been renamed to `mod_id` and `mod_name` respectively
- `dye_recipes`, `custom_recipes`, `wood_recipes` fields renamed to just `recipes` in their respective files

# 0.1.3 (2024-11-23)
- Fixed support for BetterX log & bark
  - Recipe types now use a map to translate recipe type into values to use in the output files

# 0.1.2 (2024-11-3)

## Added
- Custom recipe now has an optional `side_product` field, which creates an additional resulting item after a cutting recipe
  - Works similarly to the one in the `replace_single_recipe` override

## Changed
- The value for the custom recipe `filename` field should no longer end in `.json`
- Updated [template.json](template.json) to reflect the above changes

# 0.1.1b (2024-11-2)

## Changed
- File cleanup now only deletes the `data` folder instead of the entire directory for multiple platforms

# 0.1.1a (2024-10-31)

## Added
- Added `enable_logging` option to control file operation logging per mod
  - Defaults to `false` if not specified
  - Controls both cleanup and generation messages
  - Errors are always logged regardless of setting
  - See [template.json](template.json) for reference

## Changed
- Fixed dye recipe filenames to include `_dye` suffix for tag-based recipes
- Refactored file operations for better maintainability

# 0.1.1 (2024-10-29)

## Added
- `stem` and `hyphae` recipe types

## Changed
- Simplified version string format for single-platform builds
  - Before: `1.20.1-1.0-fabric`
  - After: `1.20.1-1.0` (when only one platform)
- Updated [template.json](template.json) custom recipe format
