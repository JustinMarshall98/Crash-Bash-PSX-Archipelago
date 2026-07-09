import typing

from typing import TYPE_CHECKING
from NetUtils import ClientStatus
from collections import Counter
import random
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .utils import Constants
from .items import item_id_to_item_name
from .locations import get_location_id_for_trophy, get_location_id_for_gem, get_location_id_for_crystal, get_location_id_for_gold_relic, get_location_id_for_plat_relic, get_location_id_for_boss
#from .options import 
from .version import __version__
from .minigames import Minigame, all_minigames

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from NetUtils import JSONMessagePart

MAIN_RAM: typing.Final[str] = "MainRAM"

class CRASHBASHClient(BizHawkClient):
    game: str = Constants.GAME_NAME
    system: str = "PSX"
    patch_suffix: str = ".apcrashbash"
    local_checked_locations: typing.Set[int]
    checked_version_string: bool

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:

        try:
            # this import down here to prevent circular import issue
            from CommonClient import logger
            # Check ROM name/patch version
            rom_name_bytes = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x9244, 8, MAIN_RAM)]))[0])
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            #info(rom_name + " rom_name")
            if not rom_name.startswith("CRASHBSH"):
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b111 # Has this been set correctly? A little confusion
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        logger.info(f"Crash Bash Client v{__version__}.")
        # Add updates section to logger info
        return True
    
    # For Trophies / Gems / Crystals
    # Read location is the ram offset for first of that minigame reward type (defined in constants)
    async def read_challenge_wins(self, ctx: "BizHawkClientContext", read_location: int) -> typing.List[bool]:
        # byte_list: typing.List[bytes] = []
        wins_list: typing.List[bool] = []
        for game_offset in range(31):
            byte: bytes = (await bizhawk.read(
                ctx.bizhawk_ctx, [(read_location + game_offset, 1, MAIN_RAM)]
            ))[0]
            wins_list.append(bool(int.from_bytes(byte)))
        return wins_list
    
    # Relics are handled differently than the other reward types
    # Although currently I am not checking for Platinum Relic Wins, so it doesn't matter atm
    async def read_relic_challenge_wins(self, ctx: "BizHawkClientContext") -> typing.List[bool]:
        wins_list: typing.List[bool] = []
        for game_offset in range(31):
            byte: bytes = (await bizhawk.read(
                ctx.bizhawk_ctx, [(Constants.GOLD_RELIC_LOCATION_OFFSET + game_offset, 1, MAIN_RAM)]
            ))[0]
            wins_list.append(bool(int.from_bytes(byte)))
        return wins_list
    
    # Also handled differently from other reward types
    async def read_boss_challenge_wins(self, ctx: "BizHawkClientContext") -> typing.List[bool]:
        # byte_list: typing.List[bytes] = []
        wins_list: typing.List[bool] = []
        byte: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx, [(Constants.PAPU_PUMMEL_LOCATION_OFFSET, 1, MAIN_RAM)]
        ))[0]
        wins_list.append(bool(int.from_bytes(byte)))
        byte = (await bizhawk.read(
            ctx.bizhawk_ctx, [(Constants.BEARMINATOR_LOCATION_OFFSET, 1, MAIN_RAM)]
        ))[0]
        wins_list.append(bool(int.from_bytes(byte)))
        byte = (await bizhawk.read(
            ctx.bizhawk_ctx, [(Constants.BIG_BAD_FOX_LOCATION_OFFSET, 1, MAIN_RAM)]
        ))[0]
        wins_list.append(bool(int.from_bytes(byte)))
        byte = (await bizhawk.read(
            ctx.bizhawk_ctx, [(Constants.OXIDE_RIDE_LOCATION_OFFSET, 1, MAIN_RAM)]
        ))[0]
        wins_list.append(bool(int.from_bytes(byte)))
        return wins_list
    

    # Don't read or write anything unless we're in the proper game mode
    # I need to figure out a better way to check for this, this check also flags on for the following:
    # Battle, Tournament, and when the main menu jumps into a minigame preview
    async def in_adventure_mode_check(self, ctx: "BizHawkClientContext") -> bool:
        # Debugging
        from CommonClient import logger
        verification_bytes: bytes = b'\x01\x01\x01'
        ram_bytes: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx, [(Constants.ADVENTURE_MODE_VERIFICATION_OFFSET, 3, MAIN_RAM)]
        ))[0]
        #logger.info(verification_bytes)
        #logger.info(ram_bytes)
        #logger.info(verification_bytes == ram_bytes)
        if verification_bytes == ram_bytes:
            return True
        return False

    async def update_reward_amounts(self, ctx: "BizHawkClientContext", trophies: int, gems: int, crystals: int, gold_relics: int, plat_relics: int) -> None:
        if trophies > 0:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.TROPHY_COUNT_OFFSET,
                        [trophies],
                        MAIN_RAM
                    )])
        if gems > 0:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.GEM_COUNT_OFFSET,
                        [gems],
                        MAIN_RAM
                    )])
        if crystals > 0:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.CRYSTAL_COUNT_OFFSET,
                        [crystals],
                        MAIN_RAM
                    )])
        if gold_relics > 0:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.GOLD_RELIC_COUNT_OFFSET,
                        [gold_relics],
                        MAIN_RAM
                    )])
    
    async def update_warp_unlocks(self, ctx: "BizHawkClientContext", warp2: bool, warp3: bool, warp4: bool, warp5: bool) -> None:
        if warp2:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.WARP_2_OFFSET,
                        [0x01],
                        MAIN_RAM
                    )])
        if warp3:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.WARP_3_OFFSET,
                        [0x01],
                        MAIN_RAM
                    )])
        if warp4:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.WARP_4_OFFSET,
                        [0x01],
                        MAIN_RAM
                    )])
        if warp5:
            await bizhawk.write(ctx.bizhawk_ctx, [(
                        Constants.WARP_5_OFFSET,
                        [0x01],
                        MAIN_RAM
                    )])


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.slot_data is not None:

            # Goal check
            if not ctx.finished_game and any((item.item == Constants.VICTORY_ITEM_ID) for item in ctx.items_received):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True

            # Debugging
            from CommonClient import logger

            # Check that the player is in adventure mode before doing anything
            if (await self.in_adventure_mode_check(ctx)):
                #new_local_check_locations: typing.Set[int]

                trophy_wins: typing.List[bool] = await self.read_challenge_wins(ctx, Constants.TROPHY_LOCATION_OFFSET)
                gem_wins: typing.List[bool] = await self.read_challenge_wins(ctx, Constants.GEM_LOCATION_OFFSET)
                crystal_wins: typing.List[bool] = await self.read_challenge_wins(ctx, Constants.CRYSTAL_LOCATION_OFFSET)
                boss_wins: typing.List[bool] = await self.read_boss_challenge_wins(ctx)

                minigames_to_trophies: typing.Dict[Minigame, bool] = {
                    minigame: hasWon for minigame, hasWon in zip(all_minigames, trophy_wins)
                }

                #new_trophy_check_locations = set([
                new_local_check_locations: typing.Set[int] = set([
                    get_location_id_for_trophy(key) for key, value in minigames_to_trophies.items() if value
                ])

                #new_local_check_locations = new_local_check_locations.union(new_trophy_check_locations)

                minigames_to_gems: typing.Dict[Minigame, bool] = {
                    minigame: hasWon for minigame, hasWon in zip(all_minigames, gem_wins)
                }

                new_gem_check_locations = set([
                    get_location_id_for_gem(key) for key, value in minigames_to_gems.items() if value
                ])

                new_local_check_locations = new_local_check_locations.union(new_gem_check_locations)

                minigames_to_crystals: typing.Dict[Minigame, bool] = {
                    minigame: hasWon for minigame, hasWon in zip(all_minigames, crystal_wins)
                }

                new_crystal_check_locations = set([
                    get_location_id_for_crystal(key) for key, value in minigames_to_crystals.items() if value
                ])

                new_local_check_locations = new_local_check_locations.union(new_crystal_check_locations)

                bosses_to_wins: typing.Dict[Minigame, bool] = {
                    all_minigames[4]: boss_wins[0], #Papu Pummel
                    all_minigames[22]: boss_wins[1], #Bearminator
                    all_minigames[9]: boss_wins[2], #Big Bad Fox
                    all_minigames[31]: boss_wins[3] #Oxide Ride
                }

                new_boss_check_locations = set([
                    get_location_id_for_boss(key) for key, value in bosses_to_wins.items() if value
                ])

                new_local_check_locations = new_local_check_locations.union(new_boss_check_locations)

                # Check for goal completion to send victory item
                if ctx.slot_data[Constants.GAME_OPTIONS_KEY]['bossgoal'] == 0: # Papu Pummel goal
                    if bosses_to_wins[all_minigames[4]]: # Player has won this challenge
                        #new_victory_check_location = set[(
                        #    Constants.VICTORY_LOCATION_ID
                        #)]
                        #new_local_check_locations = new_local_check_locations.union(new_victory_check_location)
                        new_local_check_locations.add(Constants.VICTORY_LOCATION_ID)
                if ctx.slot_data[Constants.GAME_OPTIONS_KEY]['bossgoal'] == 1: # Bearminator goal
                    if bosses_to_wins[all_minigames[22]]: # Player has won this challenge
                        #new_victory_check_location = set[(
                        #    Constants.VICTORY_LOCATION_ID
                        #)]
                        #new_local_check_locations = new_local_check_locations.union(new_victory_check_location)
                        new_local_check_locations.add(Constants.VICTORY_LOCATION_ID)
                if ctx.slot_data[Constants.GAME_OPTIONS_KEY]['bossgoal'] == 2: # Big Bad Fox goal
                    if bosses_to_wins[all_minigames[9]]: # Player has won this challenge
                        #new_victory_check_location = set[(
                        #    Constants.VICTORY_LOCATION_ID
                        #)]
                        #new_local_check_locations = new_local_check_locations.union(new_victory_check_location)
                        new_local_check_locations.add(Constants.VICTORY_LOCATION_ID)
                if ctx.slot_data[Constants.GAME_OPTIONS_KEY]['bossgoal'] == 3: # Oxide Ride goal
                    if bosses_to_wins[all_minigames[31]]: # Player has won this challenge
                        #new_victory_check_location = set[(
                        #    Constants.VICTORY_LOCATION_ID
                        #)]
                        #new_local_check_locations = new_local_check_locations.union(new_victory_check_location)
                        new_local_check_locations.add(Constants.VICTORY_LOCATION_ID)

                gold_relic_wins: typing.List[bool] = []
                minigames_to_gold_relics: typing.Dict[Minigame, bool] = {}
                if (ctx.slot_data[Constants.GAME_OPTIONS_KEY]['includegold']):
                    gold_relic_wins = await self.read_relic_challenge_wins(ctx)

                    minigames_to_gold_relics: typing.Dict[Minigame, bool] = {
                        minigame: hasWon for minigame, hasWon in zip(all_minigames, gold_relic_wins)
                    }

                    new_gold_relic_check_locations = set([
                        get_location_id_for_gold_relic(key) for key, value in minigames_to_gold_relics.items() if value
                    ])

                    new_local_check_locations = new_local_check_locations.union(new_gold_relic_check_locations)
            
                # Local checked checks handling
                if new_local_check_locations != self.local_checked_locations:
                    self.local_checked_locations = new_local_check_locations
                    if new_local_check_locations is not None:
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": list(new_local_check_locations)
                        }])

                # Read and write received items

                trophy_count: int = 0
                gem_count: int = 0
                crystal_count: int = 0
                gold_relic_count: int = 0
                plat_relic_count: int = 0
                warp_2_unlock: bool = False
                warp_3_unlock: bool = False
                warp_4_unlock: bool = False
                warp_5_unlock: bool = False

                for item in ctx.items_received:
                    if item.item == Constants.TROPHY_ITEM_ID:
                        trophy_count+= 1
                    elif item.item == Constants.GEM_ITEM_ID:
                        gem_count+= 1
                    elif item.item == Constants.CRYSTAL_ITEM_ID:
                        crystal_count+= 1
                    elif item.item == Constants.GOLD_RELIC_ITEM_ID:
                        gold_relic_count+= 1
                    elif item.item == Constants.WARP_2_ITEM_ID:
                        warp_2_unlock = True
                    elif item.item == Constants.WARP_3_ITEM_ID:
                        warp_3_unlock = True
                    elif item.item == Constants.WARP_4_ITEM_ID:
                        warp_4_unlock = True
                    elif item.item == Constants.WARP_5_ITEM_ID:
                        warp_5_unlock = True

                await self.update_reward_amounts(ctx, trophy_count, gem_count, crystal_count, gold_relic_count, plat_relic_count)
                await self.update_warp_unlocks(ctx, warp_2_unlock, warp_3_unlock, warp_4_unlock, warp_5_unlock)