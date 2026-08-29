from json import tool
from pathlib import Path
from typing import Dict

TOOL_ACTIONS = {
    "axe": "axe_dig",
    "axe_strip": "axe_strip",
    "hoe": "hoe_dig",
    "pickaxe": "pickaxe_dig",
    "shovel": "shovel_dig"
}

PLATFORM_TYPE_KEYS = {
    "fabric": "fabric:type" ,
    "neoforge": "type"
}

KNIFE_TOOL_TAG = "#c:tools/knife"
SHEARS_TOOL_TAG = "#c:tools/shears"
STRIPPING_SOUND = "minecraft:item.axe.strip"

OVERRIDE_TYPES = {
    "RECIPE_TYPES": "replace_recipe_types",
    "SINGLE_RECIPE": "replace_single_recipe"
}

class RecipeBuilder:
    def __init__(self, platform: str = None):
        self._platform = platform
        self._recipe = None

    def _recipe_exists(self):
        if self._recipe is None:
            raise ValueError("No recipe has been created yet. Call 'create_new' first.")

    def create_new(self, platform: str = "fabric"):
        self._recipe = {"type": "farmersdelight:cutting"}
        self._platform = platform

    def clear_recipe(self):
        """Clear the current recipe."""
        self._recipe = None

    def set_tool(self, tool: str = None, tag: str = None):
        """Sets the current recipe's item ability and tool. Must specify least one of tool or tag."""
        self._recipe_exists()
        if not tool and not tag:
            raise ValueError("Either 'tool' or 'tag' must be provided.")
        else:
            self._recipe["tool"] = []

        if tool: 
            type_key = PLATFORM_TYPE_KEYS[self._platform]
            self._recipe["tool"].append( 
                {
                    type_key: "farmersdelight:item_ability",
                    "action": TOOL_ACTIONS[tool]
                }
            )
        if tag:
            self._recipe["tool"].append( 
                {
                    "tag": tag
                }
            )

    def set_sound(self, sound_id: str):
        """Sets the current recipe's sound."""
        self._recipe_exists()
        self._recipe["sound"] = {
            "sound_id": sound_id
        }

    def add_ingredient(self, ingredient_value: str):
        """Add an ingredient to the current recipe."""
        self._recipe_exists()
        if "ingredients" not in self._recipe:
            self._recipe["ingredients"] = []
        self._recipe["ingredients"].append(ingredient_value)

    def add_result(self, item_id: str, count: int = 1):
        """Create a standard recipe result structure."""
        self._recipe_exists()
        self._recipe.update({
            "result": {
                "item": {
                    "count": count,
                    "id": item_id
                }
            }
        })

    def get_recipe(self) -> Dict:
        """Return the current recipe."""
        self._recipe_exists()
        if not self._recipe.get("result"):
            raise ValueError("The recipe does not have a result defined. Call 'add_result' first.")
        elif not self._recipe.get("tool"):
            raise ValueError("The recipe does not have a tool or item ability defined. Call 'set_tool' first.")

        return self._recipe

    

    # def generate_cutting_recipe(mod_data: ModData, wood_type: str, platform: str, 
    #                         recipe_map: RecipeTypeMapping, wood_override: Optional[Dict] = None) -> Dict:
    # """Generate a single cutting recipe for a specific wood type and recipe type."""

    #     # Ingredient override handling
    #     # default_ingredient = recipe_map.get_ingredient_id(mod_data.mod_id, wood_type)
    #     # ingredient = wood_override.get('ingredient', default_ingredient) if wood_override else default_ingredient

    #     if recipe_map.recipe_type in RECIPE_TYPES["SALVAGING"]:
    #         recipe["result"] = [
    #             create_recipe_result(recipe_map.get_result_id(mod_data.mod_id, wood_type))
    #         ]
    #     elif recipe_map.recipe_type in RECIPE_TYPES["STRIPPING"]:
    #         default_stripped = recipe_map.get_result_id(mod_data.mod_id, wood_type)
    #         stripped_item = wood_override.get('result', default_stripped) if wood_override else default_stripped
    #         bark_item = wood_override.get('side_product', "farmersdelight:tree_bark") if wood_override else "farmersdelight:tree_bark"
            
    #         recipe["result"] = [
    #             create_recipe_result(stripped_item),
    #             create_recipe_result(bark_item)
    #         ]
    #         recipe["sound"] = {"sound_id": STRIPPING_SOUND}
    #         recipe["tool"] = set_item_ability(platform, TOOL_ACTIONS["axe_strip"])

    #     return recipe

# def process_wood_recipes(mod_data: ModData, wood_type: str, platform: str, output_dir: Path):
#     """Process wood recipes for a specific wood type."""
#     # Check for recipe type override
#     # type_override = find_override(mod_data.recipes.overrides, 
#     #                             OVERRIDE_TYPES["RECIPE_TYPES"], 
#     #                             wood=wood_type)
    
#     # current_recipe_types = type_override['recipe_types'] if type_override else mod_data.recipes.recipe_types
#     current_recipe_types = mod_data.recipes.recipe_types

#     for recipe_type in current_recipe_types:
#         recipe_map = get_recipe_mapping(recipe_type)

#         # Check for single recipe override
#         # recipe_override = find_override(mod_data.recipes.overrides, 
#         #                               OVERRIDE_TYPES["SINGLE_RECIPE"], 
#         #                               wood=wood_type, 
#         #                               recipe_type=recipe_type)
        
#         # Create override dict with only the specified fields
#         # wood_override = get_override_fields(recipe_override, ['ingredient', 'result', 'side_product'])
#         recipe = generate_cutting_recipe(mod_data, wood_type, platform, recipe_map)
        
#         # filepath: Path = str(output_dir) + "/" + f"{recipe_map.get_file_name(wood_type)}.json"
#         # if not write_json(filepath, recipe, log_enabled=mod_data.enable_logging):
#         #     continue

