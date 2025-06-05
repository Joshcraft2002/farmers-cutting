from pathlib import Path
from typing import Dict
import shutil
import json
from .beet import generate_beet_files
from .config import load_generator_config, get_logging_setting
from .utils import cleanup_old_files, copy_tree
from .mod import process_mod_config
from .models import ModData

def process_mods(generator_config: Dict) -> None:
    """Process all mods in configuration."""

    # Clean up old files for each mod
    for mod in generator_config['mods']:
        enable_logging = get_logging_setting(mod)
        cleanup_old_files(mod, enable_logging)

    # Process each mod
    for mod in generator_config['mods']:
        process_mod_config(mod, generator_config['pack_format'], generator_config['minecraft_version'])

def generate_fccollection(generator_config: Dict):
    """Compile all generated recipes into a single collection."""

    enable_logging=generator_config.get('enable_logging', False)

    # Clear up the previous collection files
    cleanup_old_files("fccollection", enable_logging)

    # Determine all supported platforms from mod configurations
    platforms = set()
    for mod in generator_config['mods']:
        mod_config_dir = Path(__file__).parent.parent / "config" / mod
        mod_info = json.load(open(mod_config_dir / 'mod.json', encoding='utf-8'))
        platforms.update(mod_info.get('platforms', ['fabric']))

        for platform in platforms:
            mod_data_dir = Path(f"{mod}/{platform}/data/fc{mod_info['id_suffix']}")
            collection_data_dir = Path(f"fccollection/{platform}/data/fc{mod_info['id_suffix']}")
            copy_tree(mod_data_dir, collection_data_dir)

    # Send fccollection data as a "ModData" object for beet file generation
    fccollection_data = ModData(
        mod_id="fccollection",
        mod_name="Collection",
        id_suffix="collection",
        platforms=platforms,
        recipes=None,  # Irrelevant for the beet files
        data_pack_version=generator_config['fccollection_version'],
        pack_format=generator_config['pack_format'],
        enable_logging=enable_logging
    )

    for platform in platforms:
        generate_beet_files(
            Path(f"fccollection/{platform}"),
            fccollection_data,
            platform,
            generator_config["minecraft_version"],
            "All Farmer's Cutting recipes combined"
            )

def main():
    try:
        generator_config = load_generator_config()
        process_mods(generator_config)
        generate_fccollection(generator_config)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")