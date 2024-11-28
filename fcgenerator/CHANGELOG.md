# 0.1.3-bp1 (2024-11-23)

## Fixes
- fixed support for BetterX log & bark
  - recipe types now use a map to translate recipe type into values to use in the output files

# 0.1.2-bp1 (2024-11-21)

## Changed
- Backport for 1.20.1

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
