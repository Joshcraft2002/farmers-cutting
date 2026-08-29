from dataclasses import dataclass

RECIPE_TYPES = {
    "SALVAGING_FURNITURE": ["door", "hanging_sign", "sign", "trapdoor"],
    "SALVAGING_OTHER": ["chest_boat"],
    "STRIPPING": ["log", "wood", "bx_log", "bx_bark", "stem", "hyphae"]
}

@dataclass
class WoodRecipeTypeMapping:
    """Template formatted recipe type data for wood. (e.g. BetterX woods have different id formats)"""
    file_name: str
    ingredient_id: str
    results: list[str]

RECIPE_TYPE_MAPPINGS = {
    "salvaging": WoodRecipeTypeMapping(
        file_name="{wood}_{recipe_type}",
        ingredient_id="{namespace}:{wood}_{recipe_type}",
        results="{namespace}:{wood}_{recipe_type}"
    ),
    "stripping": WoodRecipeTypeMapping(
        file_name="{wood}_{recipe_type}",
        ingredient_id="{namespace}:{wood}_{recipe_type}",
        results="{namespace}:{wood}_{recipe_type}"
    ),
    # BetterX types
    "bx_log": WoodRecipeTypeMapping(
        file_name="{wood}_log",
        ingredient_id="{namespace}:{wood}_log",
        results="{namespace}:{wood}_stripped_log"
    ),
    "bx_bark": WoodRecipeTypeMapping(
        file_name="{wood}_bark",
        ingredient_id="{namespace}:{wood}_bark",
        results="{namespace}:stripped_{wood}_stripped_bark"
    )
}

class WoodRecipe:
    """Representation of an individual wood recipe"""
    def __init__(self, recipe_type: str, namespace: str, wood: str):
        if recipe_type in RECIPE_TYPES["SALVAGING"]:
            self._recipe_mapping = RECIPE_TYPE_MAPPINGS.get(recipe_type, RECIPE_TYPE_MAPPINGS["salvaging"])
        elif recipe_type in RECIPE_TYPES["STRIPPING"]:
            self._recipe_mapping = RECIPE_TYPE_MAPPINGS.get(recipe_type, RECIPE_TYPE_MAPPINGS["stripping"])
        else:
            raise ValueError(f"Unknown recipe type: {recipe_type}")

        self._namespace = namespace
        self._wood = wood

    def get_file_name(self) -> str:
        """Get formatted file name."""
        return self._recipe_mapping.file_name.format(wood=self._wood)

    def get_ingredient_id(self) -> str:
        """Get formatted ingredient path."""
        return self._recipe_mapping.ingredient_id.format(namespace=self._namespace, wood=self._wood)
    
    def get_result_id(self) -> str:
        """Get formatted result path."""
        return self._recipe_mapping.result_id.format(namespace=self._namespace, wood=self._wood)