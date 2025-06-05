from pathlib import Path
from .models import ModData
from .utils import write_json_file

def generate_beet_files(
    base_dir: Path, 
    mod_data: ModData, 
    platform: str, 
    minecraft_version: str,
    description: str = None
    ):
    """Generate beet-build.json and beet.json for a given mod and platform."""

    version = f"{minecraft_version}-{mod_data.data_pack_version}-{platform}"
    desc = description or f"Adds Farmer's Delight cutting recipes for {mod_data.mod_name}"
    
    beet_build = {
        "id": f"farmers-cutting-{mod_data.id_suffix}",
        "name": f"Farmer's Cutting: {mod_data.mod_name}",
        "version": version,
        "output": "build",
        "data_pack": {
            "pack_format": mod_data.pack_format,
            "description": desc,
            "load": ["."],
            "zipped": True
        }
    }

    beet = {
        "id": f"farmers-cutting-{mod_data.id_suffix}",
        "name": f"Farmer's Cutting: {mod_data.mod_name}",
        "version": version,
        "data_pack": {
            "pack_format": mod_data.pack_format,
            "description": desc,
            "load": ["."]
        }
    }

    write_json_file(base_dir / "beet-build.json", beet_build, log_enabled=mod_data.enable_logging)
    write_json_file(base_dir / "beet.json", beet, log_enabled=mod_data.enable_logging)