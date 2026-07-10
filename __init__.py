import typing
import warnings
import Utils
import json
import os
import settings

from worlds.AutoWorld import World, WebWorld
from BaseClasses import CollectionState, Region, Tutorial
from worlds.generic.Rules import set_rule

from .version import __version__
from .utils import Constants
from .options import CRASHBASHOptions
from .minigames import Minigame, all_minigames
from .locations import TrophyLocation, GemLocation, CrystalLocation, GoldRelicLocation, PlatinumRelicLocation, BossLocation, VictoryLocation, location_name_to_id as location_map
from .warpunlocks import all_warp_unlocks
from .items import CRASHBASHItem, create_victory_event, create_item as fabricate_item, item_name_to_item_id
from .rom import CRASHBASHProcedurePatch
from .client import CRASHBASHClient

class CRASHBASHSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Crash Bash rom"""
        description = "Crash Bash rom File"
        copy_to = "Crash Bash.bin"
        md5s = ["637F2286B1071D42F883E5592CF2DF69"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = False

class CRASHBASHWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to playing {Constants.GAME_NAME} with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jumza"]
    )

    tutorials = [setup_en]

class CRASHBASHWorld(World):
    """Crash Bash is a 2000 party video game developed by Eurocom Entertainment Software in association with
    Cerny Games and published by Sony Computer Entertainment for the PlayStation."""
    game: str = Constants.GAME_NAME
    options_dataclass = CRASHBASHOptions
    options: CRASHBASHOptions
    required_client_version = (0, 5, 0)
    web = CRASHBASHWeb()
    settings: typing.ClassVar[CRASHBASHSettings]

    #location_name_groups = location_groups

    location_name_to_id = location_map
    item_name_to_id = item_name_to_item_id

    def generate_output(self, output_directory: str) -> None:
        patch_dict: dict[str, typing.Any] = dict()
        patch_dict["TrophyRounds"] = self.options.trophyrounds.value

        rom_name_text = f"CRASHBASH{Utils.__version__.replace(".","")[0:3]}_{self.player}_{self.multiworld.seed:9}"
        rom_name_text = rom_name_text[:20]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        patch_dict["RomName"] = f'CRASHBASH{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:9}'

        patch_dict["OutputFile"] = f'{self.multiworld.get_out_file_name_base(self.player)}'

        patch = CRASHBASHProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("patch_file.json", json.dumps(patch_dict).encode("UTF-8"))
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def generate_early(self) -> None:
        # Start the player off knowing they have Warp Room 1 unlocked
        self.push_precollected(self.create_item(str(all_warp_unlocks[0])))


    def create_item(self, name: str) -> CRASHBASHItem:
        return fabricate_item(name, self.player)
    
    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)

        warp_1_region = Region("Warp 1", self.player, self.multiworld)
        warp_2_region = Region("Warp 2", self.player, self.multiworld)
        warp_3_region = Region("Warp 3", self.player, self.multiworld)
        warp_4_region = Region("Warp 4", self.player, self.multiworld)
        warp_5_region = Region("Warp 5", self.player, self.multiworld)

        # Add minigame locations for their respective Warp Rooms

        # could use major refactor lol, lots of redundancy for first go at it that I'll later squish down

        for minigame in all_minigames:
            if minigame.warpRoom == 1 and not minigame.isBoss:
                trophy_location: TrophyLocation = TrophyLocation(warp_1_region, self.player, minigame)
                set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[0]), self.player)))
                warp_1_region.locations.append(trophy_location)

                gem_location: GemLocation = GemLocation(warp_1_region, self.player, minigame)
                set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[0]), self.player)))
                warp_1_region.locations.append(gem_location)

                crystal_location: CrystalLocation = CrystalLocation(warp_1_region, self.player, minigame)
                set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[0]), self.player)))
                warp_1_region.locations.append(crystal_location)

                if self.options.includegold:
                    gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_1_region, self.player, minigame)
                    set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[0]), self.player)
                                                                                    and state.has(str(all_warp_unlocks[3]), self.player)))
                    warp_1_region.locations.append(gold_relic_location)

            elif minigame.warpRoom == 1 and minigame.isBoss:
                boss_location: BossLocation = BossLocation(warp_1_region, self.player, minigame)
                # Papu Pummel requires the player to have 4 trophies and Warp Room 1 unlocked
                set_rule(boss_location, (lambda state, t=boss_location: state.has(str(all_warp_unlocks[0]), self.player)
                                                                    and state.has(Constants.TROPHY_ITEM_NAME, self.player, 4)))
                warp_1_region.locations.append(boss_location)
                # If Papu Pummel is the players goal, set the locked Victory Item here
                if self.options.bossgoal == options.BossGoal.option_papu_papu:
                    #boss_location.place_locked_item(create_victory_event(self.player))
                    victory_location: VictoryLocation = VictoryLocation(warp_1_region, self.player)
                    set_rule(victory_location, (lambda state, t=victory_location: state.has(str(all_warp_unlocks[0]), self.player)
                                                                    and state.has(Constants.TROPHY_ITEM_NAME, self.player, 4)))
                    warp_1_region.locations.append(victory_location)
                    victory_location.place_locked_item(create_victory_event(self.player))
                    
            elif minigame.warpRoom == 2 and not minigame.isBoss:
                trophy_location: TrophyLocation = TrophyLocation(warp_2_region, self.player, minigame)
                set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[1]), self.player)))
                warp_2_region.locations.append(trophy_location)

                gem_location: GemLocation = GemLocation(warp_2_region, self.player, minigame)
                set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[1]), self.player)))
                warp_2_region.locations.append(gem_location)

                crystal_location: CrystalLocation = CrystalLocation(warp_2_region, self.player, minigame)
                set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[1]), self.player)))
                warp_2_region.locations.append(crystal_location)

                if self.options.includegold:
                    gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_2_region, self.player, minigame)
                    set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[1]), self.player)
                                                                                    and state.has(str(all_warp_unlocks[3]), self.player)))
                    warp_2_region.locations.append(gold_relic_location)

            elif minigame.warpRoom == 2 and minigame.isBoss:
                boss_location: BossLocation = BossLocation(warp_2_region, self.player, minigame)
                # Bearminator requires the player to have 9 trophies, 6 gems, 3 crystals and Warp Room 2 unlocked
                set_rule(boss_location, (lambda state, t=boss_location: state.has(str(all_warp_unlocks[1]), self.player)
                                                                    and state.has(Constants.TROPHY_ITEM_NAME, self.player, 9)
                                                                    and state.has(Constants.GEM_ITEM_NAME, self.player, 6)
                                                                    and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 3)))
                warp_2_region.locations.append(boss_location)
                # If Bearminator is the players goal, set the locked Victory Item here
                if self.options.bossgoal == options.BossGoal.option_bearminator:
                    #boss_location.place_locked_item(create_victory_event(self.player))
                    victory_location: VictoryLocation = VictoryLocation(warp_2_region, self.player)
                    set_rule(victory_location, (lambda state, t=victory_location: state.has(str(all_warp_unlocks[1]), self.player)
                                                                    and state.has(Constants.TROPHY_ITEM_NAME, self.player, 9)
                                                                    and state.has(Constants.GEM_ITEM_NAME, self.player, 6)
                                                                    and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 3)))
                    warp_2_region.locations.append(victory_location)
                    victory_location.place_locked_item(create_victory_event(self.player))
            elif minigame.warpRoom == 3 and not minigame.isBoss:
                trophy_location: TrophyLocation = TrophyLocation(warp_3_region, self.player, minigame)
                if minigame.gameName == "Metal Fox": # Metal Fox also has receiving Warp Room 2 as a requirement
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[2]), self.player)
                                                                    and state.has(str(all_warp_unlocks[1]), self.player)))
                else:
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[2]), self.player)))
                warp_3_region.locations.append(trophy_location)

                gem_location: GemLocation = GemLocation(warp_3_region, self.player, minigame)
                if minigame.gameName == "Metal Fox":
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[2]), self.player)
                                                                    and state.has(str(all_warp_unlocks[1]), self.player)))
                else:
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[2]), self.player)))
                warp_3_region.locations.append(gem_location)

                crystal_location: CrystalLocation = CrystalLocation(warp_3_region, self.player, minigame)
                if minigame.gameName == "Metal Fox":
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[2]), self.player)
                                                                    and state.has(str(all_warp_unlocks[1]), self.player)))
                else:
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[2]), self.player)))
                warp_3_region.locations.append(crystal_location)

                if self.options.includegold:
                    gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_3_region, self.player, minigame)
                    if minigame.gameName == "Metal Fox":
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[2]), self.player)
                                                                                        and state.has(str(all_warp_unlocks[3]), self.player)
                                                                                        and state.has(str(all_warp_unlocks[1]), self.player)))
                    else:
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[2]), self.player)
                                                                                        and state.has(str(all_warp_unlocks[3]), self.player)))
                    warp_3_region.locations.append(gold_relic_location)

            elif minigame.warpRoom == 3 and minigame.isBoss:
                boss_location: BossLocation = BossLocation(warp_3_region, self.player, minigame)
                # Big Bad Fox requires the player to have 15 trophies, 10 gems, 7 crystals and Warp Room 3 unlocked
                set_rule(boss_location, (lambda state, t=boss_location: state.has(str(all_warp_unlocks[2]), self.player)
                                                                    and state.has(Constants.TROPHY_ITEM_NAME, self.player, 15)
                                                                    and state.has(Constants.GEM_ITEM_NAME, self.player, 10)
                                                                    and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 7)))
                warp_3_region.locations.append(boss_location)
                # If Big Bad Fox is the players goal, set the locked Victory Item here
                if self.options.bossgoal == options.BossGoal.option_komodo_brothers:
                    #boss_location.place_locked_item(create_victory_event(self.player))
                    victory_location: VictoryLocation = VictoryLocation(warp_3_region, self.player)
                    set_rule(victory_location, (lambda state, t=victory_location: state.has(str(all_warp_unlocks[2]), self.player)
                                                                    and state.has(Constants.TROPHY_ITEM_NAME, self.player, 15)
                                                                    and state.has(Constants.GEM_ITEM_NAME, self.player, 10)
                                                                    and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 7)))
                    warp_3_region.locations.append(victory_location)
                    victory_location.place_locked_item(create_victory_event(self.player))
            elif minigame.warpRoom == 4 and not minigame.isBoss:
                trophy_location: TrophyLocation = TrophyLocation(warp_4_region, self.player, minigame)
                if minigame.gameName == "Jungle Fox": # Jungle Fox also has receiving Warp Room 2 as a requirement
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                    and state.has(str(all_warp_unlocks[1]), self.player)))
                elif minigame.gameName == "Toxic Dash": # Toxic Dash also has receiving Warp Room 3 as a requirement
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                    and state.has(str(all_warp_unlocks[2]), self.player)))
                else:
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[3]), self.player)))
                warp_4_region.locations.append(trophy_location)

                gem_location: GemLocation = GemLocation(warp_4_region, self.player, minigame)
                if minigame.gameName == "Jungle Fox":
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                    and state.has(str(all_warp_unlocks[1]), self.player)))
                elif minigame.gameName == "Toxic Dash":
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                    and state.has(str(all_warp_unlocks[2]), self.player)))
                else:
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[3]), self.player)))
                warp_4_region.locations.append(gem_location)

                crystal_location: CrystalLocation = CrystalLocation(warp_4_region, self.player, minigame)
                if minigame.gameName == "Jungle Fox":
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                    and state.has(str(all_warp_unlocks[1]), self.player)))
                elif minigame.gameName == "Toxic Dash":
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                    and state.has(str(all_warp_unlocks[2]), self.player)))
                else:
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[3]), self.player)))
                warp_4_region.locations.append(crystal_location)

                if self.options.includegold:
                    gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_4_region, self.player, minigame)
                    if minigame.gameName == "Jungle Fox":
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                                        and state.has(str(all_warp_unlocks[1]), self.player)))
                    elif minigame.gameName == "Toxic Dash":
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                                        and state.has(str(all_warp_unlocks[2]), self.player)))
                    else:
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[3]), self.player)))
                    warp_4_region.locations.append(gold_relic_location)

            elif minigame.warpRoom == 4 and minigame.isBoss:
                boss_location: BossLocation = BossLocation(warp_4_region, self.player, minigame)
                # Oxide Ride requires the player to have 22 trophies, 15 gems, 12 crystals and Warp Room 4 unlocked
                set_rule(boss_location, (lambda state, t=boss_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                    and state.has(Constants.TROPHY_ITEM_NAME, self.player, 22)
                                                                    and state.has(Constants.GEM_ITEM_NAME, self.player, 15)
                                                                    and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 12)))
                warp_4_region.locations.append(boss_location)
                # If Oxide Ride is the players goal, set the locked Victory Item here
                if self.options.bossgoal == options.BossGoal.option_nitros_oxide:
                    #boss_location.place_locked_item(create_victory_event(self.player))
                    victory_location: VictoryLocation = VictoryLocation(warp_4_region, self.player)
                    set_rule(victory_location, (lambda state, t=victory_location: state.has(str(all_warp_unlocks[3]), self.player)
                                                                    and state.has(Constants.TROPHY_ITEM_NAME, self.player, 22)
                                                                    and state.has(Constants.GEM_ITEM_NAME, self.player, 15)
                                                                    and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 12)))
                    warp_4_region.locations.append(victory_location)
                    victory_location.place_locked_item(create_victory_event(self.player))
            else:
                # Warp 5 Minigames all have extra requirements and no boss level
                # Do not include Splash Dash, Dante's Dash or Mallet Mash locations unless gold relic locations are on
                if minigame.gameName == "Splash Dash" and self.options.includegold: # Splash Dash also has receiving Warp Room 3 as a requirement
                    trophy_location: TrophyLocation = TrophyLocation(warp_5_region, self.player, minigame)
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GOLD_RELIC_ITEM_NAME, self.player, 17)
                                                                            and state.has(str(all_warp_unlocks[2]), self.player)))
                    warp_5_region.locations.append(trophy_location)
                elif minigame.gameName == "Dante's Dash" and self.options.includegold: # Dante's Dash also has receiving Warp Room 3 as a requirement
                    trophy_location: TrophyLocation = TrophyLocation(warp_5_region, self.player, minigame)
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.TROPHY_ITEM_NAME, self.player, 27)
                                                                            and state.has(str(all_warp_unlocks[2]), self.player)))
                    warp_5_region.locations.append(trophy_location)
                elif minigame.gameName == "Mallet Mash" and self.options.includegold:
                    trophy_location: TrophyLocation = TrophyLocation(warp_5_region, self.player, minigame)
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GOLD_RELIC_ITEM_NAME, self.player, 21)))
                    warp_5_region.locations.append(trophy_location)
                elif minigame.gameName == "Dragon Drop":
                    trophy_location: TrophyLocation = TrophyLocation(warp_5_region, self.player, minigame)
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 19)))
                    warp_5_region.locations.append(trophy_location)
                elif minigame.gameName == "Swamp Fox":
                    trophy_location: TrophyLocation = TrophyLocation(warp_5_region, self.player, minigame)
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 23)))
                    warp_5_region.locations.append(trophy_location)
                elif minigame.gameName == "Keg Kaboom":
                    trophy_location: TrophyLocation = TrophyLocation(warp_5_region, self.player, minigame)
                    set_rule(trophy_location, (lambda state, t=trophy_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GEM_ITEM_NAME, self.player, 25)))
                    warp_5_region.locations.append(trophy_location)
                

                if minigame.gameName == "Splash Dash" and self.options.includegold:
                    gem_location: GemLocation = GemLocation(warp_5_region, self.player, minigame)
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GOLD_RELIC_ITEM_NAME, self.player, 17)
                                                                            and state.has(str(all_warp_unlocks[2]), self.player)))
                    warp_5_region.locations.append(gem_location)
                elif minigame.gameName == "Dante's Dash" and self.options.includegold:
                    gem_location: GemLocation = GemLocation(warp_5_region, self.player, minigame)
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.TROPHY_ITEM_NAME, self.player, 27)
                                                                            and state.has(str(all_warp_unlocks[2]), self.player)))
                    warp_5_region.locations.append(gem_location)
                elif minigame.gameName == "Mallet Mash" and self.options.includegold:
                    gem_location: GemLocation = GemLocation(warp_5_region, self.player, minigame)
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GOLD_RELIC_ITEM_NAME, self.player, 21)))
                    warp_5_region.locations.append(gem_location)
                elif minigame.gameName == "Dragon Drop":
                    gem_location: GemLocation = GemLocation(warp_5_region, self.player, minigame)
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 19)))
                    warp_5_region.locations.append(gem_location)
                elif minigame.gameName == "Swamp Fox":
                    gem_location: GemLocation = GemLocation(warp_5_region, self.player, minigame)
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 23)))
                    warp_5_region.locations.append(gem_location)
                elif minigame.gameName == "Keg Kaboom":
                    gem_location: GemLocation = GemLocation(warp_5_region, self.player, minigame)
                    set_rule(gem_location, (lambda state, t=gem_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GEM_ITEM_NAME, self.player, 25)))
                    warp_5_region.locations.append(gem_location)

                if minigame.gameName == "Splash Dash" and self.options.includegold:
                    crystal_location: CrystalLocation = CrystalLocation(warp_5_region, self.player, minigame)
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GOLD_RELIC_ITEM_NAME, self.player, 17)
                                                                            and state.has(str(all_warp_unlocks[2]), self.player)))
                    warp_5_region.locations.append(crystal_location)
                elif minigame.gameName == "Dante's Dash" and self.options.includegold:
                    crystal_location: CrystalLocation = CrystalLocation(warp_5_region, self.player, minigame)
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.TROPHY_ITEM_NAME, self.player, 27)
                                                                            and state.has(str(all_warp_unlocks[2]), self.player)))
                    warp_5_region.locations.append(crystal_location)
                elif minigame.gameName == "Mallet Mash" and self.options.includegold:
                    crystal_location: CrystalLocation = CrystalLocation(warp_5_region, self.player, minigame)
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GOLD_RELIC_ITEM_NAME, self.player, 21)))
                    warp_5_region.locations.append(crystal_location)
                elif minigame.gameName == "Dragon Drop":
                    crystal_location: CrystalLocation = CrystalLocation(warp_5_region, self.player, minigame)
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 19)))
                    warp_5_region.locations.append(crystal_location)
                elif minigame.gameName == "Swamp Fox":
                    crystal_location: CrystalLocation = CrystalLocation(warp_5_region, self.player, minigame)
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 23)))
                    warp_5_region.locations.append(crystal_location)
                elif minigame.gameName == "Keg Kaboom":
                    crystal_location: CrystalLocation = CrystalLocation(warp_5_region, self.player, minigame)
                    set_rule(crystal_location, (lambda state, t=crystal_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                            and state.has(Constants.GEM_ITEM_NAME, self.player, 25)))
                    warp_5_region.locations.append(crystal_location)
                

                if self.options.includegold:
                    if minigame.gameName == "Splash Dash" and self.options.includegold: # These includegold checks are redundant here lol
                        gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_5_region, self.player, minigame)
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                                and state.has(Constants.GOLD_RELIC_ITEM_NAME, self.player, 17)
                                                                                and state.has(str(all_warp_unlocks[2]), self.player)
                                                                                and state.has(str(all_warp_unlocks[3]), self.player)))
                        warp_5_region.locations.append(gold_relic_location)
                    elif minigame.gameName == "Dante's Dash" and self.options.includegold:
                        gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_5_region, self.player, minigame)
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                                and state.has(Constants.TROPHY_ITEM_NAME, self.player, 27)
                                                                                and state.has(str(all_warp_unlocks[2]), self.player)
                                                                                and state.has(str(all_warp_unlocks[3]), self.player)))
                        warp_5_region.locations.append(gold_relic_location)
                    elif minigame.gameName == "Mallet Mash" and self.options.includegold:
                        gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_5_region, self.player, minigame)
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                                and state.has(Constants.GOLD_RELIC_ITEM_NAME, self.player, 21)
                                                                                and state.has(str(all_warp_unlocks[3]), self.player)))
                        warp_5_region.locations.append(gold_relic_location)
                    elif minigame.gameName == "Dragon Drop":
                        gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_5_region, self.player, minigame)
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                                and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 19)
                                                                                and state.has(str(all_warp_unlocks[3]), self.player)))
                        warp_5_region.locations.append(gold_relic_location)
                    elif minigame.gameName == "Swamp Fox":
                        gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_5_region, self.player, minigame)
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                                and state.has(Constants.CRYSTAL_ITEM_NAME, self.player, 23)
                                                                                and state.has(str(all_warp_unlocks[3]), self.player)))
                        warp_5_region.locations.append(gold_relic_location)
                    elif minigame.gameName == "Keg Kaboom":
                        gold_relic_location: GoldRelicLocation = GoldRelicLocation(warp_5_region, self.player, minigame)
                        set_rule(gold_relic_location, (lambda state, t=gold_relic_location: state.has(str(all_warp_unlocks[4]), self.player)
                                                                                and state.has(Constants.GEM_ITEM_NAME, self.player, 25)
                                                                                and state.has(str(all_warp_unlocks[3]), self.player)))
                        warp_5_region.locations.append(gold_relic_location)
                    

        # Set completion condition
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            Constants.VICTORY_ITEM_NAME, self.player
        )

        # Connect regions
        menu_region.connect(warp_1_region)
        warp_1_region.connect(
            warp_2_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[1]), self.player)
        )
        warp_1_region.connect(
            warp_3_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[2]), self.player)
        )
        warp_1_region.connect(
            warp_4_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[3]), self.player)
        )
        warp_1_region.connect(
            warp_5_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[4]), self.player)
        )
        warp_2_region.connect(
            warp_3_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[2]), self.player)
        )
        warp_2_region.connect(
            warp_4_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[3]), self.player)
        )
        warp_2_region.connect(
            warp_5_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[4]), self.player)
        )
        warp_3_region.connect(
            warp_4_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[3]), self.player)
        )
        warp_3_region.connect(
            warp_5_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[4]), self.player)
        )
        warp_4_region.connect(
            warp_5_region,
            None,
            lambda state: state.has(str(all_warp_unlocks[4]), self.player)
        )
        self.multiworld.regions.append(warp_1_region)
        self.multiworld.regions.append(warp_2_region)
        self.multiworld.regions.append(warp_3_region)
        self.multiworld.regions.append(warp_4_region)
        self.multiworld.regions.append(warp_5_region)
        self.multiworld.regions.append(menu_region)

    def create_items(self) -> None:
        itempool: typing.List[CRASHBASHItem] = []

        # Non boss minigame items
        for minigame in all_minigames:
            if minigame.warpRoom < 5 and not minigame.isBoss:
                # Create Trophies, Gems and Crystals for all these minigames, Relics if the options are on
                itempool.append(self.create_item(Constants.TROPHY_ITEM_NAME))
                itempool.append(self.create_item(Constants.GEM_ITEM_NAME))
                itempool.append(self.create_item(Constants.CRYSTAL_ITEM_NAME))
                if self.options.includegold:
                    itempool.append(self.create_item(Constants.GOLD_RELIC_ITEM_NAME))
            elif minigame.warpRoom == 5:
                if minigame.gameName == "Splash Dash" or minigame.gameName == "Dante's Dash" or minigame.gameName == "Mallet Mash":
                    if self.options.includegold:
                        itempool.append(self.create_item(Constants.TROPHY_ITEM_NAME))
                        itempool.append(self.create_item(Constants.GEM_ITEM_NAME))
                        itempool.append(self.create_item(Constants.CRYSTAL_ITEM_NAME))
                        itempool.append(self.create_item(Constants.GOLD_RELIC_ITEM_NAME))
                else:
                    itempool.append(self.create_item(Constants.TROPHY_ITEM_NAME))
                    itempool.append(self.create_item(Constants.GEM_ITEM_NAME))
                    itempool.append(self.create_item(Constants.CRYSTAL_ITEM_NAME))
                    if self.options.includegold:
                        itempool.append(self.create_item(Constants.GOLD_RELIC_ITEM_NAME))
        
        # Boss items, the warp unlocks
        itempool.append(self.create_item(str(all_warp_unlocks[1])))
        itempool.append(self.create_item(str(all_warp_unlocks[2])))
        itempool.append(self.create_item(str(all_warp_unlocks[3])))
        itempool.append(self.create_item(str(all_warp_unlocks[4])))

        # No filler right now

        self.multiworld.itempool.extend(itempool)

    # No filler right now
#    def get_filler_item_name(self) -> str:
        

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            Constants.GENERATED_WITH_KEY: __version__,
            Constants.GAME_OPTIONS_KEY: self.options.serialize()
        }
