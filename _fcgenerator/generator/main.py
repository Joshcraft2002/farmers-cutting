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

def generate_collection(generator_config: Dict):
    """Compile all generated recipes into a single collection."""

    collection_config = generator_config.get('collection_data')
    collection_data = ModData(
        mod_id=collection_config['mod_id'],
        mod_name=collection_config['mod_name'],
        id_suffix=collection_config['id_suffix'],
        platforms=None, 
        recipes=None,  # Both Irrelevant for this
        data_pack_version=collection_config['data_pack_version'],
        pack_format=generator_config['pack_format'],
        max_inclusive_pack_format=collection_config.get('max_inclusive_pack_format', None),
        enable_logging=collection_config.get('enable_logging', False)
    )

    # Clear up the previous collection files
    cleanup_old_files(f"fc{collection_data.mod_id}", collection_data.enable_logging)

    # Determine all supported platforms from mod configurations
    platforms = set()
    for mod in generator_config['mods']:
        mod_config_dir = Path(__file__).parent.parent / "config" / mod
        mod_info = json.load(open(mod_config_dir / 'mod.json', encoding='utf-8'))
        platforms.update(mod_info.get('platforms', ['fabric']))

        for platform in platforms:
            mod_data_dir = Path(f"{mod}/{platform}/data/fc{mod_info['id_suffix']}")
            collection_data_dir = Path(f"fc{collection_data.mod_id}/{platform}/data/fc{mod_info['id_suffix']}")
            copy_tree(mod_data_dir, collection_data_dir)

    for platform in platforms:
        generate_beet_files(
            Path(f"fc{collection_data.mod_id}/{platform}"),
            collection_data,
            platform,
            generator_config["minecraft_version"],
            collection_config["description"]
            )

def main():
    try:
        generator_config = load_generator_config()
        process_mods(generator_config)
        if generator_config['create_collection']:
            generate_collection(generator_config)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")