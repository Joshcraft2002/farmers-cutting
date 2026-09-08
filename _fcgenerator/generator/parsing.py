from .models import *
from typing import Dict
from .fcfilerw import read_json

# Functions kept separate in case of formatting changes between versions

def parse_mod_data(mod_data: Dict, minecraft_version: str) -> ModData:
    return ModData(
        mod_id=mod_data['mod_id'],
        mod_name=mod_data['mod_name'],
        id_suffix=mod_data['id_suffix'],
        version_data=VersionData(
            minecraft_version=minecraft_version,
            data_pack_version=mod_data['data_pack_version'],
            min_format=mod_data['min_format'],
            max_format=mod_data['max_format']
        ),
        platforms=mod_data.get('platforms'),
        recipes=ModRecipes(
            wood_recipes=[],
            dye_recipes=[],
            overrides=[],
            custom_recipes=[]
        ),
        enable_logging=mod_data.get('enable_logging', False)
    )

def parse_wood_recipes(wood_data_json: Dict, mod_data: ModData):
    """Parse wood recipes from wood recipe json into recipes in ModData"""
    try:
        parsed_recipes = []
        wood_recipes: list[Dict] = wood_data_json.get('recipes', [])
        overrides: list = []
        # overrides = wood_data_json.get('overrides', [])
        for recipe_set in wood_recipes:
            recipe_types = recipe_set.get('types', {})
            wood_recipe_set = WoodRecipeSet(
                woods=recipe_set.get('woods', []),
                furniture=recipe_types.get('furniture', []),
                salvaging=recipe_types.get('salvaging', []),
                cutting=recipe_types.get('cutting', [])
            )
            parsed_recipes.append(wood_recipe_set)
    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f"Error parsing wood recipes: {e}. Proceeding with empty recipes.")
        parsed_recipes = []
        overrides = []
    finally:
        mod_data.recipes.wood_recipes = parsed_recipes
        mod_data.recipes.overrides = overrides

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