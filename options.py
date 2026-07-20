import typing
import dataclasses

from Options import Range, Choice, PerGameCommonOptions, Toggle as DefaultOffToggle
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
    """
    display_name = "Trophy Rounds"
    range_start = 1
    range_end = 5
    default = 3

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
    PLEASE NOTE this option is not yet implemented.
    Activating this option has no effect on the game currently.

    Platinum Relic challenges will become locations.
    Platinum Relics will be shuffled into the multiworld.
    """
    display_name = "Include Platinum Relics"
    

@dataclass
class CRASHBASHOptions(PerGameCommonOptions):
    bossgoal: BossGoal
    trophyrounds: TrophyRounds
    includegold: IncludeGoldRelics
    includeplat: IncludePlatinumRelics
      
    def serialize(self) -> typing.Dict[str, int]:
        return_dict: typing.Dict[str, int] = {}
        for field in dataclasses.fields(self):
            if field.name != "plando_items":
                return_dict[field.name] = getattr(self, field.name).value
        return return_dict
    #def serialize(self) -> typing.Dict[str, int]:
    #    return {field.name: getattr(self, field.name).value for field in dataclasses.fields(self)}