import typing

from dataclasses import dataclass

@dataclass
class Constants:
    # CRASH BASH constants!
    GAME_NAME: str = "Crash Bash"

    VICTORY_ITEM_ID: int = 0x01
    VICTORY_ITEM_NAME: str = "Crash Bashed"
    VICTORY_LOCATION_NAME: str = "Crash Bashed"
    VICTORY_LOCATION_ID: int = 0x0C

    ADVENTURE_MODE_VERIFICATION_OFFSET: int = 0x5A671

    WARP_2_OFFSET: int = 0x5A781
    WARP_3_OFFSET: int = 0x5A793
    WARP_4_OFFSET: int = 0x5A786
    WARP_5_OFFSET: int = 0x5A79C
    TROPHY_COUNT_OFFSET: int = 0x5A782
    GEM_COUNT_OFFSET: int = 0x5A783
    CRYSTAL_COUNT_OFFSET: int = 0x5A784
    GOLD_RELIC_COUNT_OFFSET: int = 0x5A787
    PLAT_RELIC_COUNT_OFFSET: int = 0x5A788

    TROPHY_LOCATION_OFFSET: int = 0x5A6F8
    GEM_LOCATION_OFFSET: int = 0x5A73A
    CRYSTAL_LOCATION_OFFSET: int = 0x5A75B
    GOLD_RELIC_LOCATION_OFFSET: int = 0x5A719 # Note that Platinum Relic locations in game use the same offset as gold
    PLAT_RELIC_LOCATION_OFFSET: int = 0x100 # But for AP, Platinum Relic locations need separate ID's
    PAPU_PUMMEL_LOCATION_OFFSET: int = 0x5A780
    BIG_BAD_FOX_LOCATION_OFFSET: int = 0x5A785
    BEARMINATOR_LOCATION_OFFSET: int = 0x5A792
    OXIDE_RIDE_LOCATION_OFFSET: int = 0x5A79B

    WARP_1_ITEM_ID: int = 0x02
    WARP_2_ITEM_ID: int = 0x03
    WARP_3_ITEM_ID: int = 0x04
    WARP_4_ITEM_ID: int = 0x05
    WARP_5_ITEM_ID: int = 0x06
    TROPHY_ITEM_ID: int = 0x07
    GEM_ITEM_ID: int = 0x08
    CRYSTAL_ITEM_ID: int = 0x09
    GOLD_RELIC_ITEM_ID: int = 0x0A
    PLAT_RELIC_ITEM_ID: int = 0x0B

    TROPHY_ITEM_NAME: str = "Trophy"
    GEM_ITEM_NAME: str = "Gem"
    CRYSTAL_ITEM_NAME: str = "Crystal"
    GOLD_RELIC_ITEM_NAME: str = "Gold Relic"
    PLAT_RELIC_ITEM_NAME: str = "Platinum Relic"

    TROPHY_ROUNDS_ROM_OFFSET: int = 0x5052FFC

    GENERATED_WITH_KEY: str = "k"
    GAME_OPTIONS_KEY: str = "g"