from pathlib import Path
from typing import Dict
import json

CONFIG_DIR = Path(__file__).parent.parent / "config"
GENERATOR_CONFIG = "generator.json"
DEFAULT_PLATFORM = "fabric"

def read_json_config(path: Path) -> Dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_generator_config() -> Dict:
    """Load the generator-wide configuration (mods list, MC version)."""
    config_path = CONFIG_DIR / GENERATOR_CONFIG
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)

def get_logging_setting(mod: str) -> bool:
    """Load logging setting for a specific mod."""
    mod_config_dir = CONFIG_DIR / mod
    try:
        mod_info = read_json_config(mod_config_dir / 'mod.json')
        return mod_info.get('enable_logging', False)
    except (FileNotFoundError, ValueError):
        return False  # Default to False if can't read config