from pathlib import Path
import shutil
from typing import Dict

from .recipe.wood import generate_wood_recipes
# from .beet import generate_beet_files
from .fcfilerw import read_json, PATH_DIR
from .models import ModData, ModRecipes
from .fcfilerw import copy_dir_tree

DEFAULT_PLATFORM = "fabric"

def process_mod_data(mod_id: str, minecraft_version: str):
    """Parse mod data into readable structure"""
    mod_data_dir = PATH_DIR / mod_id
    
    try:
        # Load required mod.json
        mod_info = read_json(mod_data_dir / 'mod.json')

        # Setup overall mod data
        recipes = ModRecipes(
            woods_recipes=[],
            dye_recipes=[],
            overrides=[],
            custom_recipes=[]
        )
        mod_data = ModData(
            mod_id=mod_info['mod_id'],
            mod_name=mod_info['mod_name'],
            id_suffix=mod_info['id_suffix'],
            minecraft_version=minecraft_version,
            data_pack_version=mod_info['data_pack_version'],
            min_format=mod_info['min_format'],
            max_format=mod_info['max_format'],
            platforms=mod_info.get('platforms', [DEFAULT_PLATFORM]),
            recipes=recipes,
            enable_logging=mod_info.get('enable_logging', False)
        )        

        # Parse recipe files
        parse_wood_recipes(mod_data_dir / 'wood.json', mod_data)
        parse_dye_recipes(mod_data_dir / 'dye.json', mod_data)
        parse_custom_recipes(mod_data_dir / 'custom.json', mod_data)

        generate_mod_files(mod_data)

    except FileNotFoundError as e:
        print(f"Error: Required configuration file not found: {e}")
        return
    except Exception as e:
        print(f"Error processing mod '{mod_id}': {e}")
        return

def parse_wood_recipes(wood_data_json: Dict, mod_data: ModData):
    """Parse wood recipes from mod data json into ModData object"""
    recipes = mod_data.recipes
    try:
        wood_info = read_json(wood_data_json)
        wood_recipes = wood_info.get('recipes', [])
        overrides = wood_info.get('overrides', [])
    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f"Error parsing wood recipes: {e}. Proceeding with empty recipes.")
        wood_recipes = []
        overrides = []
    recipes.wood_recipes = wood_recipes
    recipes.overrides = overrides

def parse_dye_recipes(dye_data_json: Dict, mod_data: ModData):
    try:
        dye_info = read_json(dye_data_json)
        dye_recipes = dye_info.get('recipes', [])
    except (FileNotFoundError, ValueError) as e:
        print(f"Error parsing dye recipes: {e}. Proceeding with empty recipes.")
        dye_recipes = []
    mod_data.recipes.dye_recipes = dye_recipes

def parse_custom_recipes(custom_data_json: Dict, mod_data: ModData):
    try:
        custom_info = read_json(custom_data_json)
        custom_recipes = custom_info.get('recipes', [])
    except (FileNotFoundError, ValueError) as e:
        print(f"Error parsing custom recipes: {e}. Proceeding with empty recipes.")
        custom_recipes = []
    mod_data.recipes.custom_recipes = custom_recipes
    
def copy_extras(mod_id: str, platform: str, output_data_dir: Path):
    """Copy all extra files."""
    extras_dir = PATH_DIR / mod_id / "extras" / platform
    copy_dir_tree(extras_dir, output_data_dir)

def generate_mod_files(mod_data: ModData):
    print(f"files generated for mod: {mod_data.mod_name}")

    for platform in mod_data.platforms:
        recipe_dir = get_recipe_dir(mod_data, platform)
        recipe_dir.mkdir(parents=True, exist_ok=True)

        generate_wood_recipes(mod_data, platform, recipe_dir)
        # generate_recipes(mod_data, platform, recipe_dir)
        # copy_extras(mod_data.mod_id, platform, mod_data_dir)
        # generate_beet_files(base_dir, mod_data, platform, minecraft_version)

def get_recipe_dir(mod_data: ModData, platform: str) -> Path:
    """Get the recipe directory for a given mod and platform."""
    base_dir = Path(f"{mod_data.mod_id}/{platform}")
    recipe_dir = base_dir / 'data' / f"fc{mod_data.id_suffix}" / 'recipe'
    return recipe_dir
        