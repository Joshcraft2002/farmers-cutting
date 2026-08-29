from pathlib import Path
from typing import Dict, List, Optional
from models import ModData, WoodRecipeSet
from recipetype import WoodRecipe, WoodRecipeType
from fcfilerw import write_json

from builder import TOOL_ACTIONS, PLATFORMS, KNIFE_TOOL_TAG, STRIPPING_SOUND, OVERRIDE_TYPES, RecipeBuilder

TREE_BARK_ITEM = "farmersdelight:tree_bark"

def generate_cutting_recipe(recipe_builder: RecipeBuilder, mod_data: ModData, wood_type: str,  
                            recipe_type: WoodRecipeType, wood_override: Optional[Dict] = None) -> Dict:
    """Generate a single cutting recipe for a specific wood type and recipe type."""

    # Ingredient override handling
    default_ingredient = recipe_type.get_ingredient_id(mod_data.mod_id, wood_type)
    ingredient = wood_override.get('ingredient', default_ingredient) if wood_override else default_ingredient
    
    recipe_builder.add_ingredient(ingredient)
        

def generate_salvaging_recipe(recipe_builder: RecipeBuilder, mod_data: ModData) -> Dict:
    # recipe_builder.clear_recipe()
    # recipe_builder.add_result(recipe_map.get_result_id(mod_data.mod_id, wood_type))
    # recipe_builder.set_tool("axe")
    pass

def generate_stripping_recipes(recipe_builder: RecipeBuilder, recipe_set: WoodRecipeSet, mod_data: ModData, output_dir: Path):
    for wood_type in recipe_set:
        for recipe_type in recipe_set.stripping:
            wood_recipe = WoodRecipe(recipe_type, mod_data.mod_id, wood_type)
            recipe_builder.clear_recipe()

            # default_stripped = recipe_map.get_result_id(mod_data.mod_id, wood_type)
            # stripped_item = wood_override.get('result', default_stripped) if wood_override else default_stripped
            stripped_item = wood_recipe.get_result_id()

            #bark_item = wood_override.get('side_product', "farmersdelight:tree_bark") if wood_override else "farmersdelight:tree_bark"
            bark_item = TREE_BARK_ITEM
            
            recipe_builder.add_result(stripped_item)
            recipe_builder.add_result(bark_item)
            recipe_builder.set_sound(STRIPPING_SOUND)
            recipe_builder.set_tool("axe_strip")

            path = str(output_dir) + "/" + f"{wood_recipe.get_file_name()}.json"
            write_json(path, recipe_builder.get_recipe(), mod_data.enable_logging)   

def generate_furniture_recipe():
    pass

def generate_wood_recipes(mod_data: ModData, platform: str, output_dir: Path):
    """Process wood recipes for a specific wood type."""
    
    recipe_builder = RecipeBuilder(platform)
    # Check for recipe type override
    # type_override = find_override(mod_data.recipes.overrides, 
    #                             OVERRIDE_TYPES["RECIPE_TYPES"], 
    #                             wood=wood_type)
    
    # current_recipe_types = type_override['recipe_types'] if type_override else mod_data.recipes.recipe_types
    wood_recipes = mod_data.recipes.wood_recipes

    # For every wood type in each RecipeSet, generate recipes for each recipe type
    for recipe_set in wood_recipes:
        generate_stripping_recipes(recipe_builder, recipe_set, mod_data, output_dir)
    
        # Check for single recipe override
        # recipe_override = find_override(mod_data.recipes.overrides, 
        #                               OVERRIDE_TYPES["SINGLE_RECIPE"], 
        #                               wood=wood_type, 
        #                               recipe_type=recipe_type)
        
        # Create override dict with only the specified fields
        # wood_override = get_override_fields(recipe_override, ['ingredient', 'result', 'side_product'])
        # recipe = generate_cutting_recipe(recipe, mod_data, wood_type, wood_recipe_type)
        
        # filepath: Path = str(output_dir) + "/" + f"{wood_recipe.get_file_name()}.json"
        # if not write_json(filepath, recipe, log_enabled=mod_data.enable_logging):
        #     continue