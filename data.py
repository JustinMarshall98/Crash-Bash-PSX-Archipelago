from .minigames import all_minigames, Minigame
from .locations import get_location_name_for_trophy, get_location_name_for_gem, get_location_name_for_crystal, get_location_name_for_gold_relic, get_location_name_for_plat_relic, get_location_name_for_boss

# Location Groups - By Minigame Type
#Ballistix
ballistix: list[Minigame] = [
    all_minigames[14],
    all_minigames[15],
    all_minigames[16],
    all_minigames[17]
]
ballistix_locations: list[str] = []
for game in ballistix:
    ballistix_locations.append(get_location_name_for_trophy(game))
    ballistix_locations.append(get_location_name_for_gem(game))
    ballistix_locations.append(get_location_name_for_crystal(game))
    ballistix_locations.append(get_location_name_for_gold_relic(game))
    #ballistix_locations.append(get_location_name_for_plat_relic(game))
#Polar Push
polar_push: list[Minigame] = [
    all_minigames[18],
    all_minigames[19],
    all_minigames[20],
    all_minigames[21]
]
polar_push_locations: list[str] = []
for game in polar_push:
    polar_push_locations.append(get_location_name_for_trophy(game))
    polar_push_locations.append(get_location_name_for_gem(game))
    polar_push_locations.append(get_location_name_for_crystal(game))
    polar_push_locations.append(get_location_name_for_gold_relic(game))
    #polar_push_locations.append(get_location_name_for_plat_relic(game))
#Pogo Pandemonium
pogo_pandemonium: list[Minigame] = [
    all_minigames[10],
    all_minigames[11],
    all_minigames[12],
    all_minigames[13]
]
pogo_pandemonium_locations: list[str] = []
for game in pogo_pandemonium:
    pogo_pandemonium_locations.append(get_location_name_for_trophy(game))
    pogo_pandemonium_locations.append(get_location_name_for_gem(game))
    pogo_pandemonium_locations.append(get_location_name_for_crystal(game))
    pogo_pandemonium_locations.append(get_location_name_for_gold_relic(game))
    #pogo_pandemonium_locations.append(get_location_name_for_plat_relic(game))
#Crate Crush
crate_crush: list[Minigame] = [
    all_minigames[0],
    all_minigames[1],
    all_minigames[2],
    all_minigames[3]
]
crate_crush_locations: list[str] = []
for game in crate_crush:
    crate_crush_locations.append(get_location_name_for_trophy(game))
    crate_crush_locations.append(get_location_name_for_gem(game))
    crate_crush_locations.append(get_location_name_for_crystal(game))
    crate_crush_locations.append(get_location_name_for_gold_relic(game))
    #crate_crush_locations.append(get_location_name_for_plat_relic(game))
#Tank Wars
tank_wars: list[Minigame] = [
    all_minigames[5],
    all_minigames[6],
    all_minigames[7],
    all_minigames[8]
]
tank_wars_locations: list[str] = []
for game in tank_wars:
    tank_wars_locations.append(get_location_name_for_trophy(game))
    tank_wars_locations.append(get_location_name_for_gem(game))
    tank_wars_locations.append(get_location_name_for_crystal(game))
    tank_wars_locations.append(get_location_name_for_gold_relic(game))
    #tank_wars_locations.append(get_location_name_for_plat_relic(game))
#Crash Dash
crash_dash: list[Minigame] = [
    all_minigames[23],
    all_minigames[24],
    all_minigames[25],
    all_minigames[26]
]
crash_dash_locations: list[str] = []
for game in crash_dash:
    crash_dash_locations.append(get_location_name_for_trophy(game))
    crash_dash_locations.append(get_location_name_for_gem(game))
    crash_dash_locations.append(get_location_name_for_crystal(game))
    crash_dash_locations.append(get_location_name_for_gold_relic(game))
    #crash_dash_locations.append(get_location_name_for_plat_relic(game))
#Medieval Mayhem
medieval_mayhem: list[Minigame] = [
    all_minigames[27],
    all_minigames[28],
    all_minigames[29],
    all_minigames[30]
]
medieval_mayhem_locations: list[str] = []
for game in medieval_mayhem:
    medieval_mayhem_locations.append(get_location_name_for_trophy(game))
    medieval_mayhem_locations.append(get_location_name_for_gem(game))
    medieval_mayhem_locations.append(get_location_name_for_crystal(game))
    medieval_mayhem_locations.append(get_location_name_for_gold_relic(game))
    #medieval_mayhem_locations.append(get_location_name_for_plat_relic(game))
#Bosses
bosses: list[Minigame] = [
    all_minigames[4],
    all_minigames[9],
    all_minigames[22],
    all_minigames[31]
]
bosses_locations: list[str] = []
for game in bosses:
    bosses_locations.append(get_location_name_for_boss(game))

# Location Groups - By Warp Room

warp_1: list[Minigame] = [
    all_minigames[14],
    all_minigames[19],
    all_minigames[10],
    all_minigames[0],
    all_minigames[4]
]
warp_1_locations: list[str] = []
for game in warp_1:
    if not game.isBoss:
        warp_1_locations.append(get_location_name_for_trophy(game))
        warp_1_locations.append(get_location_name_for_gem(game))
        warp_1_locations.append(get_location_name_for_crystal(game))
        warp_1_locations.append(get_location_name_for_gold_relic(game))
        #warp_1_locations.append(get_location_name_for_plat_relic(game))
    else:
        warp_1_locations.append(get_location_name_for_boss(game))

warp_2: list[Minigame] = [
    all_minigames[15],
    all_minigames[18],
    all_minigames[11],
    all_minigames[1],
    all_minigames[6],
    all_minigames[22]
]
warp_2_locations: list[str] = []
for game in warp_2:
    if not game.isBoss:
        warp_2_locations.append(get_location_name_for_trophy(game))
        warp_2_locations.append(get_location_name_for_gem(game))
        warp_2_locations.append(get_location_name_for_crystal(game))
        warp_2_locations.append(get_location_name_for_gold_relic(game))
        #warp_2_locations.append(get_location_name_for_plat_relic(game))
    else:
        warp_2_locations.append(get_location_name_for_boss(game))

warp_3: list[Minigame] = [
    all_minigames[16],
    all_minigames[20],
    all_minigames[12],
    all_minigames[2],
    all_minigames[8],
    all_minigames[23],
    all_minigames[9]
]
warp_3_locations: list[str] = []
for game in warp_3:
    if not game.isBoss:
        warp_3_locations.append(get_location_name_for_trophy(game))
        warp_3_locations.append(get_location_name_for_gem(game))
        warp_3_locations.append(get_location_name_for_crystal(game))
        warp_3_locations.append(get_location_name_for_gold_relic(game))
        #warp_3_locations.append(get_location_name_for_plat_relic(game))
    else:
        warp_3_locations.append(get_location_name_for_boss(game))

warp_4: list[Minigame] = [
    all_minigames[17],
    all_minigames[21],
    all_minigames[13],
    all_minigames[3],
    all_minigames[7],
    all_minigames[24],
    all_minigames[27],
    all_minigames[31]
]
warp_4_locations: list[str] = []
for game in warp_4:
    if not game.isBoss:
        warp_4_locations.append(get_location_name_for_trophy(game))
        warp_4_locations.append(get_location_name_for_gem(game))
        warp_4_locations.append(get_location_name_for_crystal(game))
        warp_4_locations.append(get_location_name_for_gold_relic(game))
        #warp_4_locations.append(get_location_name_for_plat_relic(game))
    else:
        warp_4_locations.append(get_location_name_for_boss(game))

warp_5: list[Minigame] = [
    all_minigames[25],
    all_minigames[28],
    all_minigames[29],
    all_minigames[5],
    all_minigames[30],
    all_minigames[26]
]
warp_5_locations: list[str] = []
for game in warp_5:
    if not game.isBoss:
        warp_5_locations.append(get_location_name_for_trophy(game))
        warp_5_locations.append(get_location_name_for_gem(game))
        warp_5_locations.append(get_location_name_for_crystal(game))
        warp_5_locations.append(get_location_name_for_gold_relic(game))
        #warp_5_locations.append(get_location_name_for_plat_relic(game))
    else:
        warp_5_locations.append(get_location_name_for_boss(game))

# Location Groups - By Challenge Type
# Bosses are already their own group as defined by Minigame Type

#Trophies
trophy_locations: list[str] = []
for game in all_minigames:
    trophy_locations.append(get_location_name_for_trophy(game))

#Gems
gem_locations: list[str] = []
for game in all_minigames:
    gem_locations.append(get_location_name_for_gem(game))
    
#Crystals
crystal_locations: list[str] = []
for game in all_minigames:
    crystal_locations.append(get_location_name_for_crystal(game))
    
#Gold Relics
gold_relic_locations: list[str] = []
for game in all_minigames:
    gold_relic_locations.append(get_location_name_for_gold_relic(game))
    
#Platinum Relics
#plat_relic_locations: list[str] = []
#for game in all_minigames:
#    plat_relic_locations.append(get_location_name_for_plat_relic(game))


location_groups = {
    "Ballistix": ballistix_locations,
    "Polar Push": polar_push_locations,
    "Pogo Pandemonium": pogo_pandemonium_locations,
    "Crate Crush": crate_crush_locations,
    "Tank Wars": tank_wars_locations,
    "Crash Dash": crash_dash_locations,
    "Medieval Mayhem": medieval_mayhem_locations,
    "Bosses": bosses_locations,
    "Warp 1": warp_1_locations,
    "Warp 2": warp_2_locations,
    "Warp 3": warp_3_locations,
    "Warp 4": warp_4_locations,
    "Warp 5": warp_5_locations,
    "Trophy Challenges": trophy_locations,
    "Gem Challenges": gem_locations,
    "Crystal Challenges": crystal_locations,
    "Gold Relic Challenges": gold_relic_locations
    #"Platinum Relic Challenges": plat_relic_locations
}