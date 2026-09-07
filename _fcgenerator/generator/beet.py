from pathlib import Path
from .models import ModData
from .fcfilerw import write_json

def generate_beet_files(
    mod_data: ModData, 
    platform: str,
    base_dir: Path,
    description: str = None
    ):

    version_data = mod_data.version_data

    version = f"{version_data.minecraft_version}-{version_data.data_pack_version}-{platform}"
    desc = description or f"Adds Farmer's Delight cutting recipes for {mod_data.mod_name}"
    
    # basic beet file for testing
    data_pack = {
        "min_format": version_data.min_format,
        "max_format": version_data.max_format,
        "description": desc,
        "load": ["."]
    }

    beet = {
        "id": f"farmers-cutting-{mod_data.id_suffix}",
        "name": f"Farmer's Cutting: {mod_data.mod_name}",
        "version": version,
        "data_pack": data_pack
    }

    write_json(base_dir / "beet.json", beet, log_enabled=mod_data.enable_logging)

    # specify zipping and output dir for final build
    data_pack["zipped"] = True
    beet["output"] = "build"

    write_json(base_dir / "beet-build.json", beet, log_enabled=mod_data.enable_logging)
    