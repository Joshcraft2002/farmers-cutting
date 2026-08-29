from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ModData:
    """Name, version, and recipe data for a mod."""
    mod_id: str
    mod_name: str
    id_suffix: str
    minecraft_version: str
    data_pack_version: str
    min_format: List[int]
    max_format: List[int]
    platforms: List[str]
    recipes: ModRecipes
    enable_logging: bool = False

@dataclass
class WoodRecipeSet:
    woods: list[str]
    furniture: list[str]
    salvaging: list[str]
    stripping: list[str]

@dataclass 
class ModRecipes:
    """Recipes for a mod"""
    wood_recipes: List[WoodRecipeSet]
    dye_recipes: List[Dict[str, Any]]
    overrides: List[Dict[str, Any]]
    custom_recipes: List[Dict[str, Any]]


    

