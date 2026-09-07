from pathlib import Path
import shutil
from typing import Dict

from .beet import generate_beet_files

# from .recipe.wood import generate_wood_recipes
from .fcfilerw import read_json, PATH_DIR
from .models import ModData, ModRecipes, VersionData
from .fcfilerw import copy_dir_tree
from .parsing import *

def process_mod_data(mod_id: str, mc_version: str):
    mod_data_dir = PATH_DIR / mod_id
    
    try:
        print(f"Parsing data for mod with ID: {mod_id}")
        # Load required mod.json
        mod_info = read_json(mod_data_dir / 'mod.json')
        mod_data = parse_mod_data(mod_info, mc_version)
        print(f"Parsed mod data for {mod_data.mod_name}")

        # Parse recipe files
        # parse_wood_recipes(mod_data_dir / 'wood.json', mod_data)
        # parse_dye_recipes(mod_data_dir / 'dye.json', mod_data)
        # parse_custom_recipes(mod_data_dir / 'custom.json', mod_data)

        generate_mod_files(mod_data)

    except FileNotFoundError as e:
        print(f"Error: Required data file not found: {e}")
        return
    except Exception as e:
        print(f"Error processing mod '{mod_id}': {e}")
        return
    
def copy_extras(mod_id: str, platform: str, output_data_dir: Path):
    """Copy all extra files."""
    extras_dir = PATH_DIR / mod_id / "extras" / platform
    copy_dir_tree(extras_dir, output_data_dir)

def generate_mod_files(mod_data: ModData):
    print(f"Generating files for mod: {mod_data.mod_name}")

    for platform in mod_data.platforms:
        recipe_dir = get_recipe_dir(mod_data, platform)
        recipe_dir.mkdir(parents=True, exist_ok=True)

        # generate_wood_recipes(mod_data, platform, recipe_dir)
        # generate_recipes(mod_data, platform, recipe_dir)
        # copy_extras(mod_data.mod_id, platform, mod_data_dir)
        generate_beet_files(mod_data, platform, recipe_dir)

def get_recipe_dir(mod_data: ModData, platform: str) -> Path:
    """Get the recipe directory for a given mod and platform."""
    base_dir = Path(f"{mod_data.mod_id}/{platform}")
    recipe_dir = base_dir / 'data' / f"fc{mod_data.id_suffix}" / 'recipe'
    return recipe_dir
        