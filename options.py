import typing
import dataclasses

from Options import Range, Choice, PerGameCommonOptions, Toggle as DefaultOffToggle, DefaultOnToggle
from dataclasses import dataclass

class BossGoal(Choice):
    """
    Choose which Boss will be the goal for your game.
    The requirements for each boss is the same as the base game
    plus the required warp room to reach them.
    """
    display_name = "Goal"
    option_papu_papu = 0
    option_bearminator = 1
    option_komodo_brothers = 2
    option_nitros_oxide = 3
    default = 3

class TrophyRounds(Range):
    """
    How many rounds you must win to beat a Trophy Challenge.
    In the base game, this number is 3.
    Each trophy round you win awards a check. Adding more locations
    will allow more minigame buff items to be generated for your world.
    """
    display_name = "Trophy Rounds"
    range_start = 1
    range_end = 3
    default = 1

class IncludeGoldRelics(DefaultOffToggle):
    """
    Gold Relic challenges will become locations,
    as well as the Splash Dash, Dante's Dash and Mallet Mash minigames
    which are otherwise excluded because you can't reach them.
    Gold Relics will be shuffled into the multiworld.
    """
    display_name = "Include Gold Relics"

class IncludePlatinumRelics(DefaultOffToggle):
    """
    Platinum Relic challenges will become locations.
    These locations will allow more minigame buff items to generate for your world
    as the platinum relic items are currently useless and are not included.
    """
    display_name = "Include Platinum Relics"

class IncludeTraps(DefaultOffToggle):
    """
    Enables a small number of character swap traps to generate if there is location space.
    For more information, check out the Buffs and Traps doc.
    """
    display_name = "Include Traps"
    

@dataclass
class CRASHBASHOptions(PerGameCommonOptions):
    bossgoal: BossGoal
    trophyrounds: TrophyRounds
    includegold: IncludeGoldRelics
    includeplat: IncludePlatinumRelics
    includetrap: IncludeTraps
      
    def serialize(self) -> typing.Dict[str, int]:
        return_dict: typing.Dict[str, int] = {}
        for field in dataclasses.fields(self):
            if field.name != "plando_items":
                return_dict[field.name] = getattr(self, field.name).value
        return return_dict
    #def serialize(self) -> typing.Dict[str, int]:
    #    return {field.name: getattr(self, field.name).value for field in dataclasses.fields(self)}