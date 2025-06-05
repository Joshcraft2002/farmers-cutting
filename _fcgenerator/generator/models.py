from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass 
class ModRecipes:
    """Recipes for a mod"""
    woods: List[str]
    recipe_types: List[str]
    dye_recipes: List[Dict[str, Any]]
    overrides: List[Dict[str, Any]]
    custom_recipes: List[Dict[str, Any]]

@dataclass
class ModData:
    """Name, version, and recipe data for a mod."""
    mod_id: str
    mod_name: str
    id_suffix: str
    platforms: List[str]
    data_pack_version: str
    pack_format: int
    recipes: ModRecipes
    enable_logging: bool = False

@dataclass
class RecipeTypeMapping:
    """Mapping of values used in the recipe file per recipe type."""
    recipe_type: str
    __file_name: str
    __ingredient_id: str
    __result_id: str

    def __init__(self, recipe_type: str, file_name: str, ingredient_id: str, result_id: str):
        self.recipe_type = recipe_type
        self.__file_name = file_name
        self.__ingredient_id = ingredient_id
        self.__result_id = result_id

    def get_file_name(self, wood: str) -> str:
        """Get formatted file name."""
        return self.__file_name.format(wood=wood)

    def get_ingredient_id(self, namespace: str, wood: str) -> str:
        """Get formatted ingredient path."""
        return self.__ingredient_id.format(namespace=namespace, wood=wood)
    
    def get_result_id(self, namespace: str, wood: str) -> str:
        """Get formatted result path."""
        return self.__result_id.format(namespace=namespace, wood=wood)