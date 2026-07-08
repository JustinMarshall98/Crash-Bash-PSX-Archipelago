import typing

from BaseClasses import Location, Region, LocationProgressType, Item
from .minigames import Minigame, all_minigames
from .utils import Constants

def get_location_name_for_trophy(minigame: Minigame) -> str:
    return f"{minigame.gameName} Trophy Challenge"

def get_location_name_for_gem(minigame: Minigame) -> str:
    return f"{minigame.gameName} Gem Challenge"

def get_location_name_for_crystal(minigame: Minigame) -> str:
    return f"{minigame.gameName} Crystal Challenge"

def get_location_name_for_gold_relic(minigame: Minigame) -> str:
    return f"{minigame.gameName} Gold Relic Challenge"

def get_location_name_for_plat_relic(minigame: Minigame) -> str:
    return f"{minigame.gameName} Platinum Relic Challenge"

def get_location_name_for_boss(minigame: Minigame) -> str:
    return f"{minigame.gameName} Boss Challenge"

def get_location_id_for_trophy(minigame: Minigame) -> int:
    return Constants.TROPHY_LOCATION_OFFSET + minigame.id

def get_location_id_for_gem(minigame: Minigame) -> int:
    return Constants.GEM_LOCATION_OFFSET + minigame.id

def get_location_id_for_crystal(minigame: Minigame) -> int:
    return Constants.CRYSTAL_LOCATION_OFFSET + minigame.id

def get_location_id_for_gold_relic(minigame: Minigame) -> int:
    return Constants.GOLD_RELIC_LOCATION_OFFSET + minigame.id

def get_location_id_for_plat_relic(minigame: Minigame) -> int:
    return Constants.PLAT_RELIC_LOCATION_OFFSET + minigame.id

def get_location_id_for_boss(minigame: Minigame) -> int:
    if (minigame.gameName == "Papu Pummel"):
        return Constants.PAPU_PUMMEL_LOCATION_OFFSET
    elif (minigame.gameName == "Big Bad Fox"):
        return Constants.BIG_BAD_FOX_LOCATION_OFFSET
    elif (minigame.gameName == "Bearminator"):
        return Constants.BEARMINATOR_LOCATION_OFFSET
    else: # Oxide Ride
        return Constants.OXIDE_RIDE_LOCATION_OFFSET
    
class CRASHBASHLocation(Location):
    game: str

    def __init__(self, region: Region, player: int, name: str, id: int):
        super().__init__(player, name, parent=region)
        self.game = Constants.GAME_NAME
        self.address = id

    def exclude(self) -> None:
        self.progress_type = LocationProgressType.EXCLUDED

    def place(self, item: Item) -> None:
        self.item = item
        item.location = self

class TrophyLocation(CRASHBASHLocation):
    # Check for a completed Trophy Challenge
    minigame: Minigame

    def __init__(self, region: Region, player: int, minigame: Minigame):
        super().__init__(region, player, get_location_name_for_trophy(minigame), get_location_id_for_trophy(minigame))
        self.minigame = minigame

class GemLocation(CRASHBASHLocation):
    # Check for a completed Gem Challenge
    minigame: Minigame

    def __init__(self, region: Region, player: int, minigame: Minigame):
        super().__init__(region, player, get_location_name_for_gem(minigame), get_location_id_for_gem(minigame))
        self.minigame = minigame

class CrystalLocation(CRASHBASHLocation):
    # Check for a completed Crystal Challenge
    minigame: Minigame

    def __init__(self, region: Region, player: int, minigame: Minigame):
        super().__init__(region, player, get_location_name_for_crystal(minigame), get_location_id_for_crystal(minigame))
        self.minigame = minigame

class GoldRelicLocation(CRASHBASHLocation):
    # Check for a completed Gold Relic Challenge
    minigame: Minigame

    def __init__(self, region: Region, player: int, minigame: Minigame):
        super().__init__(region, player, get_location_name_for_gold_relic(minigame), get_location_id_for_gold_relic(minigame))
        self.minigame = minigame

class PlatinumRelicLocation(CRASHBASHLocation):
    # Check for a completed Platinum Relic Challenge
    minigame: Minigame

    def __init__(self, region: Region, player: int, minigame: Minigame):
        super().__init__(region, player, get_location_name_for_plat_relic(minigame), get_location_id_for_plat_relic(minigame))
        self.minigame = minigame

class BossLocation(CRASHBASHLocation):
    # Check for a completed Boss Challenge
    minigame: Minigame

    def __init__(self, region: Region, player: int, minigame: Minigame):
        super().__init__(region, player, get_location_name_for_boss(minigame), get_location_id_for_boss(minigame))
        self.minigame = minigame

class VictoryLocation(CRASHBASHLocation):
    # Check for game completion
    # Necessary right now because we're hard up for locations in game
    # The bosses slots are required to fit in all warps right now

    def __init__(self, region: Region, player: int):
        super().__init__(region, player, Constants.VICTORY_LOCATION_NAME, Constants.VICTORY_LOCATION_ID)

trophy_location_name_to_id: typing.Dict[str, int] = {}
gem_location_name_to_id: typing.Dict[str, int] = {}
crystal_location_name_to_id: typing.Dict[str, int] = {}
gold_relic_location_name_to_id: typing.Dict[str, int] = {}
plat_relic_location_name_to_id: typing.Dict[str, int] = {}
boss_location_name_to_id: typing.Dict[str, int] = {}
victory_location_name_to_id: typing.Dict[str, int] = {}

for minigame in all_minigames:
    trophy_location_name_to_id[get_location_name_for_trophy(minigame)] = get_location_id_for_trophy(minigame)
    gem_location_name_to_id[get_location_name_for_gem(minigame)] = get_location_id_for_gem(minigame)
    crystal_location_name_to_id[get_location_name_for_crystal(minigame)] = get_location_id_for_crystal(minigame)
    gold_relic_location_name_to_id[get_location_name_for_gold_relic(minigame)] = get_location_id_for_gold_relic(minigame)
    plat_relic_location_name_to_id[get_location_name_for_plat_relic(minigame)] = get_location_id_for_plat_relic(minigame)
    if minigame.isBoss:
        boss_location_name_to_id[get_location_name_for_boss(minigame)] = get_location_id_for_boss(minigame)
victory_location_name_to_id[Constants.VICTORY_LOCATION_NAME] = Constants.VICTORY_LOCATION_ID

location_name_to_id: typing.Dict[str, int] = {**trophy_location_name_to_id, **gem_location_name_to_id, **crystal_location_name_to_id, **gold_relic_location_name_to_id, **plat_relic_location_name_to_id, **boss_location_name_to_id, **victory_location_name_to_id}