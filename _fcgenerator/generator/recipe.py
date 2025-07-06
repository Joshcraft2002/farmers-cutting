from pathlib import Path
from typing import Dict, List, Optional
from .models import ModData, RecipeTypeMapping
from .utils import write_json_file

RECIPE_TYPE_MAPPINGS = {
    # For non-default mappings
    # BetterX types
    "bx_log": RecipeTypeMapping(
        recipe_type="bx_log",
        file_name="{wood}_log",
        ingredient_id="{namespace}:{wood}_log",
        result_id="{namespace}:{wood}_stripped_log"
    ),
    "bx_bark": RecipeTypeMapping(
        recipe_type="bx_bark",
        file_name="{wood}_bark",
        ingredient_id="{namespace}:{wood}_bark",
        result_id="{namespace}:{wood}_stripped_bark"
    )
}

RECIPE_TYPES = {
    "PLANKS_RECYCLE": ["door", "hanging_sign", "sign", "trapdoor"],
    "STRIPPING": ["log", "wood", "bx_log", "bx_bark", "stem", "hyphae"]
}

TOOL_ACTIONS = {
    "axe": "axe_dig",
    "axe_strip": "axe_strip",
    "hoe": "hoe_dig",
    "pickaxe": "pickaxe_dig",
    "shovel": "shovel_dig"
}

PLATFORMS = {
    "fabric": { "type_key": "fabric:type" },
    "neoforge": { "type_key": "type" }
}

KNIFE_TOOL_TAG = "#c:tools/knife"
SHEARS_TOOL_TAG = "#c:tools/shears"
STRIPPING_SOUND = "minecraft:item.axe.strip"

OVERRIDE_TYPES = {
    "RECIPE_TYPES": "replace_recipe_types",
    "SINGLE_RECIPE": "replace_single_recipe"
}

def find_override(overrides: List[Dict], override_type: str, **conditions) -> Optional[Dict]:
    """Find an override matching the given conditions."""
    return next((o for o in overrides 
                if o['type'] == override_type 
                and all(o.get(k) == v for k, v in conditions.items())), None)

def get_recipe_mapping(recipe_type: str) -> RecipeTypeMapping:
    """Get the mapping for a recipe type."""
    if recipe_type in RECIPE_TYPES["PLANKS_RECYCLE"]:
        return RECIPE_TYPE_MAPPINGS.get(recipe_type, 
            RecipeTypeMapping(
                recipe_type=recipe_type,
                file_name=f"{{wood}}_{recipe_type}",
                ingredient_id=f"{{namespace}}:{{wood}}_{recipe_type}",
                result_id=f"{{namespace}}:{{wood}}_planks"
            )
        )
    elif recipe_type in RECIPE_TYPES["STRIPPING"]:
        return RECIPE_TYPE_MAPPINGS.get(recipe_type, 
            RecipeTypeMapping(
                recipe_type=recipe_type,
                file_name=f"{{wood}}_{recipe_type}",
                ingredient_id=f"{{namespace}}:{{wood}}_{recipe_type}",
                result_id=f"{{namespace}}:stripped_{{wood}}_{recipe_type}"
            )
        )
    raise ValueError(f"Unknown recipe type: {recipe_type}")

def get_override_fields(override: Dict, fields: List[str]) -> Optional[Dict]:
    """Extract specified fields from an override."""
    if not override:
        return None
    return {k: v for k, v in override.items() if k in fields}

def set_item_ability(platform: str, action: str) -> Dict:
    """Get the platform-specific item ability structure."""
    platform_config = PLATFORMS[platform]
    return {
        platform_config["type_key"]: "farmersdelight:item_ability",
        "action": action
    }

def create_base_recipe(ingredient_value: str) -> Dict:
    """Create a base structure for all cutting recipes."""
    return {
        "type": "farmersdelight:cutting",
        "ingredients": [ingredient_value]
    }

def create_recipe_result(item_id: str, count: int = 1) -> Dict:
    """Create a standard recipe result structure."""
    return {
        "item": {
            "count": count,
            "id": item_id
        }
    }

def generate_cutting_recipe(mod_data: ModData, wood_type: str, platform: str, 
                            recipe_map: RecipeTypeMapping, wood_override: Optional[Dict] = None) -> Dict:
    """Generate a single cutting recipe for a specific wood type and recipe type."""

    default_ingredient = recipe_map.get_ingredient_id(mod_data.mod_id, wood_type)
    ingredient = wood_override.get('ingredient', default_ingredient) if wood_override else default_ingredient
    
    recipe = create_base_recipe(ingredient)
    recipe["tool"] = set_item_ability(platform, TOOL_ACTIONS["axe"])

    if recipe_map.recipe_type in RECIPE_TYPES["PLANKS_RECYCLE"]:
        recipe["result"] = [
            create_recipe_result(recipe_map.get_result_id(mod_data.mod_id, wood_type))
        ]
    elif recipe_map.recipe_type in RECIPE_TYPES["STRIPPING"]:
        default_stripped = recipe_map.get_result_id(mod_data.mod_id, wood_type)
        stripped_item = wood_override.get('result', default_stripped) if wood_override else default_stripped
        bark_item = wood_override.get('side_product', "farmersdelight:tree_bark") if wood_override else "farmersdelight:tree_bark"
        
        recipe["result"] = [
            create_recipe_result(stripped_item),
            create_recipe_result(bark_item)
        ]
        recipe["sound"] = {"sound_id": STRIPPING_SOUND}
        recipe["tool"] = set_item_ability(platform, TOOL_ACTIONS["axe_strip"])

    return recipe

def generate_dye_recipe(mod_id: str, input_item: str, color: str, count: int) -> Dict:   
    """Generate a single dye cutting recipe."""
    
    is_tag = input_item.startswith('#')    
    recipe = create_base_recipe(input_item if is_tag else f"{mod_id}:{input_item}")
    recipe["result"] = [
        create_recipe_result(f"minecraft:{color}_dye", count)
    ]
    recipe["tool"] = KNIFE_TOOL_TAG
    
    return recipe

def generate_custom_recipe(recipe_data: Dict, platform: str) -> Dict:
    """Generate a single custom cutting recipe."""

    recipe = create_base_recipe(recipe_data['ingredient'])
    
    recipe["result"] = [create_recipe_result(recipe_data['result'], recipe_data['count'])]
    if 'side_product' in recipe_data:
        recipe["result"].append(create_recipe_result(recipe_data['side_product']))

    if recipe_data['tool'] == "knife":
        recipe["tool"] = KNIFE_TOOL_TAG
    elif recipe_data['tool'] == "shears":
        recipe["tool"] = SHEARS_TOOL_TAG
    else:
        recipe["tool"] = set_item_ability(platform, TOOL_ACTIONS[recipe_data['tool']])

    return recipe

def process_wood_recipes(mod_data: ModData, wood_type: str, platform: str, output_dir: Path):
    """Process wood recipes for a specific wood type."""
    # Check for recipe type override
    type_override = find_override(mod_data.recipes.overrides, 
                                OVERRIDE_TYPES["RECIPE_TYPES"], 
                                wood=wood_type)
    
    current_recipe_types = type_override['recipe_types'] if type_override else mod_data.recipes.recipe_types

    for recipe_type in current_recipe_types:
        recipe_map = get_recipe_mapping(recipe_type)

        # Check for single recipe override
        recipe_override = find_override(mod_data.recipes.overrides, 
                                      OVERRIDE_TYPES["SINGLE_RECIPE"], 
                                      wood=wood_type, 
                                      recipe_type=recipe_type)
        
        # Create override dict with only the specified fields
        wood_override = get_override_fields(recipe_override, ['ingredient', 'result', 'side_product'])
        recipe = generate_cutting_recipe(mod_data, wood_type, platform, recipe_map, wood_override)
        
        filepath: Path = str(output_dir) + "/" + f"{recipe_map.get_file_name(wood_type)}.json"
        if not write_json_file(filepath, recipe, log_enabled=mod_data.enable_logging):
            continue

def generate_recipes(mod_data: ModData, platform: str, output_dir: Path):
    """Generate all recipes (wood, dye, custom) for a mod/platform."""
    # Process each type of recipe
    for wood_type in mod_data.recipes.woods:
        process_wood_recipes(mod_data, wood_type, platform, output_dir)

    # Generate dye cutting recipes
    for dye_recipe in mod_data.recipes.dye_recipes:
        input_item = dye_recipe['input']
        color = dye_recipe['color']
        count = dye_recipe['count']
        
        recipe = generate_dye_recipe(mod_data.mod_id, input_item, color, count)
        
        filename = f"{color}_dye_from_tag.json" if input_item.startswith('#') else f"{input_item}.json"
        filepath = str(output_dir) + "/" + filename
        if not write_json_file(filepath, recipe, log_enabled=mod_data.enable_logging):
            continue

    # Generate custom recipes
    for custom_recipe in mod_data.recipes.custom_recipes:
        recipe = generate_custom_recipe(custom_recipe, platform)
        filepath = str(output_dir) + "/" + f"{custom_recipe['filename']}.json"
        if not write_json_file(filepath, recipe, log_enabled=mod_data.enable_logging):
            continue