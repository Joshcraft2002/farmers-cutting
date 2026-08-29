from pathlib import Path
from typing import Dict
import shutil
import json
# from .beet import generate_beet_files
from .fcfilerw import cleanup_old_files, load_generator_data
from .mod import process_mod_data
from .models import ModData

def process_generator_data(generator_data: Dict) -> None:
    """Process all generator data."""

    # Clean up old files for each mod
    for mod in generator_data['mods']:
        # enable_logging = get_logging_setting(mod)
        cleanup_old_files(mod, False)

    # Process each mod
    for mod in generator_data['mods']:
        process_mod_data(mod, generator_data['minecraft_version'])

# TODO: ensure data format is correct
def validate_data(generator_data: Dict) -> bool:
    return True

# def generate_collection(generator_config: Dict):
#     """Compile all generated recipes into a single collection."""

#     collection_config = generator_config.get('collection_data')
#     collection_data = ModData(
#         mod_id=collection_config['mod_id'],
#         mod_name=collection_config['mod_name'],
#         id_suffix=collection_config['id_suffix'],
#         platforms=None, 
#         recipes=None,  # Both Irrelevant for this
#         data_pack_version=collection_config['data_pack_version'],
#         min_format=collection_config['min_format'],
#         max_format=collection_config['max_format'],
#         enable_logging=collection_config.get('enable_logging', False)
#     )

#     # Clear up the previous collection files
#     cleanup_old_files(f"fc{collection_data.mod_id}", collection_data.enable_logging)

#     # Determine all supported platforms from mod configurations
#     platforms = set()
#     for mod in generator_config['mods']:
#         mod_config_dir = Path(__file__).parent.parent / "config" / mod
#         mod_info = json.load(open(mod_config_dir / 'mod.json', encoding='utf-8'))
#         platforms.update(mod_info.get('platforms', ['fabric']))

#         for platform in platforms:
#             mod_data_dir = Path(f"{mod}/{platform}/data/fc{mod_info['id_suffix']}")
#             collection_data_dir = Path(f"fc{collection_data.mod_id}/{platform}/data/fc{mod_info['id_suffix']}")
#             copy_tree(mod_data_dir, collection_data_dir)

#     for platform in platforms:
#         generate_beet_files(
#             Path(f"fc{collection_data.mod_id}/{platform}"),
#             collection_data,
#             platform,
#             generator_config["minecraft_version"],
#             collection_config["description"]
#             )

def main():
    try:
        generator_data = load_generator_data()
        if not (validate_data(generator_data)):
            raise Exception("Invalid generator data format")
        # if load_generator_config()['create_collection']:
        #     generate_collection(load_generator_config())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        process_generator_data(generator_data)