from pathlib import Path
from typing import Dict, List, Optional
from .models import ModData, RecipeTypeMapping
from .fcfilerw import write_json

# def find_override(overrides: List[Dict], override_type: str, **conditions) -> Optional[Dict]:
#     """Find an override matching the given conditions."""
#     return next((o for o in overrides 
#                 if o['type'] == override_type 
#                 and all(o.get(k) == v for k, v in conditions.items())), None)

# def get_override_fields(override: Dict, fields: List[str]) -> Optional[Dict]:
#     """Extract specified fields from an override."""
#     if not override:
#         return None
#     return {k: v for k, v in override.items() if k in fields}

# def generate_dye_recipe(mod_id: str, input_item: str, color: str, count: int) -> Dict:   
#     """Generate a single dye cutting recipe."""
    
#     is_tag = input_item.startswith('#')    
#     recipe = create_base_recipe(input_item if is_tag else f"{mod_id}:{input_item}")
#     recipe["result"] = [
#         create_recipe_result(f"minecraft:{color}_dye", count)
#     ]
#     recipe["tool"] = KNIFE_TOOL_TAG
    
#     return recipe

# def generate_custom_recipe(recipe_data: Dict, platform: str) -> Dict:
#     """Generate a single custom cutting recipe."""

#     recipe = create_base_recipe(recipe_data['ingredient'])
    
#     recipe["result"] = [create_recipe_result(recipe_data['result'], recipe_data['count'])]
#     if 'side_product' in recipe_data:
#         recipe["result"].append(create_recipe_result(recipe_data['side_product']))

#     if recipe_data['tool'] == "knife":
#         recipe["tool"] = KNIFE_TOOL_TAG
#     elif recipe_data['tool'] == "shears":
#         recipe["tool"] = SHEARS_TOOL_TAG
#     else:
#         recipe["tool"] = set_item_ability(platform, TOOL_ACTIONS[recipe_data['tool']])

#     return recipe



# def generate_recipes(mod_data: ModData, platform: str, output_dir: Path):
#     """Generate all recipes (wood, dye, custom) for a mod/platform."""
#     # Process each type of recipe
#     for wood_type in mod_data.recipes.woods:
#         process_wood_recipes(mod_data, wood_type, platform, output_dir)

#     # Generate dye cutting recipes
#     for dye_recipe in mod_data.recipes.dye_recipes:
#         input_item = dye_recipe['input']
#         color = dye_recipe['color']
#         count = dye_recipe['count']
        
#         recipe = generate_dye_recipe(mod_data.mod_id, input_item, color, count)
        
#         filename = f"{color}_dye_from_tag.json" if input_item.startswith('#') else f"{input_item}.json"
#         filepath = str(output_dir) + "/" + filename
#         if not write_json_file(filepath, recipe, log_enabled=mod_data.enable_logging):
#             continue

#     # Generate custom recipes
#     for custom_recipe in mod_data.recipes.custom_recipes:
#         recipe = generate_custom_recipe(custom_recipe, platform)
#         filepath = str(output_dir) + "/" + f"{custom_recipe['filename']}.json"
#         if not write_json_file(filepath, recipe, log_enabled=mod_data.enable_logging):
#             continue