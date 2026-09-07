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
    # TODO: check if field exists
    for mod in generator_data['mods']:
        process_mod_data(mod, generator_data['minecraft_version'])

# TODO: ensure data format is correct
def validate_data(generator_data: Dict) -> bool:
    return True

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