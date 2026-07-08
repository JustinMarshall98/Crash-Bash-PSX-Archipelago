import typing

from BaseClasses import Item, ItemClassification
from .utils import Constants
from .warpunlocks import all_warp_unlocks

item_id_to_item_name: typing.Dict[int, str] = {}

item_id_to_item_name[Constants.TROPHY_ITEM_ID] = Constants.TROPHY_ITEM_NAME
item_id_to_item_name[Constants.GEM_ITEM_ID] = Constants.GEM_ITEM_NAME
item_id_to_item_name[Constants.CRYSTAL_ITEM_ID] = Constants.CRYSTAL_ITEM_NAME
item_id_to_item_name[Constants.GOLD_RELIC_ITEM_ID] = Constants.GOLD_RELIC_ITEM_NAME
item_id_to_item_name[Constants.PLAT_RELIC_ITEM_ID] = Constants.PLAT_RELIC_ITEM_NAME

item_id_to_item_name[Constants.WARP_1_ITEM_ID] = str(all_warp_unlocks[0])
item_id_to_item_name[Constants.WARP_2_ITEM_ID] = str(all_warp_unlocks[1])
item_id_to_item_name[Constants.WARP_3_ITEM_ID] = str(all_warp_unlocks[2])
item_id_to_item_name[Constants.WARP_4_ITEM_ID] = str(all_warp_unlocks[3])
item_id_to_item_name[Constants.WARP_5_ITEM_ID] = str(all_warp_unlocks[4])

item_id_to_item_name[Constants.VICTORY_ITEM_ID] = Constants.VICTORY_ITEM_NAME

item_name_to_item_id: typing.Dict[str, int] = {value: key for key, value in item_id_to_item_name.items()}

class CRASHBASHItem(Item):
    game: str = Constants.GAME_NAME

def create_item(name: str, player_id: int) -> CRASHBASHItem:
    return CRASHBASHItem(name, ItemClassification.progression, item_name_to_item_id[name], player_id) # No filler right now

def create_victory_event(player_id: int) -> CRASHBASHItem:
    return CRASHBASHItem(Constants.VICTORY_ITEM_NAME, ItemClassification.progression, Constants.VICTORY_ITEM_ID, player_id)
