from pathlib import Path
from typing import Dict
import json



# def get_logging_setting(mod: str) -> bool:
#     """Load logging setting for a specific mod."""
#     mod_config_dir = CONFIG_DIR / mod
#     try:
#         mod_info = read_json_config(mod_config_dir / 'mod.json')
#         return mod_info.get('enable_logging', False)
#     except (FileNotFoundError, ValueError):
#         return False  # Default to False if can't read config