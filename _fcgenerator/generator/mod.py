from pathlib import Path
import shutil
from .beet import generate_beet_files
from .config import read_json_config, CONFIG_DIR, DEFAULT_PLATFORM
from .models import ModData, ModRecipes
from .recipe import generate_recipes
from .utils import copy_tree

def process_mod_config(mod_id: str, minecraft_version: str):
    mod_config_dir = CONFIG_DIR / mod_id
    try:
        # Load required mod.json
        mod_info = read_json_config(mod_config_dir / 'mod.json')
        # Optional: wood.json
        try:
            wood_info = read_json_config(mod_config_dir / 'wood.json')
            woods = wood_info['recipes'].get('woods', [])
            recipe_types = wood_info['recipes'].get('types', [])
            overrides = wood_info.get('overrides', [])
        except (FileNotFoundError, ValueError, KeyError):
            woods = []
            recipe_types = []
            overrides = []
        # Optional: dye.json
        try:
            dye_info = read_json_config(mod_config_dir / 'dye.json')
            dye_recipes = dye_info.get('recipes', [])
        except (FileNotFoundError, ValueError):
            dye_recipes = []
        # Optional: custom.json
        try:
            custom_info = read_json_config(mod_config_dir / 'custom.json')
            custom_recipes = custom_info.get('recipes', [])
        except (FileNotFoundError, ValueError):
            custom_recipes = []

        recipes = ModRecipes(
            woods=woods,
            recipe_types=recipe_types,
            dye_recipes=dye_recipes,
            overrides=overrides,
            custom_recipes=custom_recipes
        )

        mod_data = ModData(
            mod_id=mod_info['mod_id'],
            mod_name=mod_info['mod_name'],
            id_suffix=mod_info['id_suffix'],
            data_pack_version=mod_info['data_pack_version'],
            min_format=mod_info['min_format'],
            max_format=mod_info['max_format'],
            platforms=mod_info.get('platforms', [DEFAULT_PLATFORM]),
            recipes= recipes,
            enable_logging=mod_info.get('enable_logging', False)
        )

        write_mod_files(mod_data, minecraft_version)

    except FileNotFoundError as e:
        print(f"Error: Required configuration file not found: {e}")
        return
    except Exception as e:
        print(f"Error processing mod '{mod_id}': {e}")
        return
    
def copy_extras(mod_id: str, platform: str, output_data_dir: Path):
    """Copy all extra files."""
    extras_dir = CONFIG_DIR / mod_id / "extras" / platform
    copy_tree(extras_dir, output_data_dir)

def write_mod_files(mod_data: ModData, minecraft_version: str):
    for platform in mod_data.platforms:
        base_dir = Path(f"{mod_data.mod_id}/{platform}")
        mod_data_dir = base_dir / 'data' / f"fc{mod_data.id_suffix}"
        recipe_dir = mod_data_dir / 'recipe'
        recipe_dir.mkdir(parents=True, exist_ok=True)
        generate_recipes(mod_data, platform, recipe_dir)
        copy_extras(mod_data.mod_id, platform, mod_data_dir)
        generate_beet_files(base_dir, mod_data, platform, minecraft_version)
        