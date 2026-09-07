from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ModData:
    mod_id: str
    mod_name: str
    id_suffix: str
    version_data: VersionData
    platforms: List[str]
    recipes: ModRecipes
    enable_logging: bool = False

@dataclass
class VersionData:
    minecraft_version: str
    data_pack_version: str
    min_format: List[int]
    max_format: List[int]

@dataclass 
class ModRecipes:
    wood_recipes: List[WoodRecipeSet]
    dye_recipes: List[Dict[str, Any]]
    overrides: List[Dict[str, Any]]
    custom_recipes: List[Dict[str, Any]]

@dataclass
class WoodRecipeSet:
    woods: list[str]
    furniture: list[str]
    salvaging: list[str]
    stripping: list[str]
    

