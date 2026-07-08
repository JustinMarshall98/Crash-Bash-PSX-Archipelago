import typing
from .utils import Constants

class Minigame:
    id: int
    gameName: str
    isBoss: bool
    warpRoom: int

    def __init__(self, _id: int, gameName: str, isBoss: bool, warpRoom: int):
        self.id = _id
        self.gameName = gameName
        self.isBoss = isBoss
        self.warpRoom = warpRoom
    
    def __str__(self) -> str:
        return (
            f"{self.gameName}"
        )
    
all_minigames: typing.Tuple[Minigame, ...] = (
    Minigame(0, "Jungle Bash", False, 1),
    Minigame(1, "Space Bash", False, 2),
    Minigame(2, "Snow Bash", False, 3),
    Minigame(3, "Drain Bash", False, 4),
    Minigame(4, "Papu Pummel", True, 1),
    Minigame(5, "Swamp Fox", False, 5),
    Minigame(6, "Desert Fox", False, 2),
    Minigame(7, "Jungle Fox", False, 4),
    Minigame(8, "Metal Fox", False, 3),
    Minigame(9, "Big Bad Fox", True, 3),
    Minigame(10, "Pogo Painter", False, 1),
    Minigame(11, "Pogo-a-Gogo", False, 2),
    Minigame(12, "El Pogo Loco", False, 3),
    Minigame(13, "Pogo Padlock", False, 4),
    Minigame(14, "Crash Ball", False, 1),
    Minigame(15, "Beach Ball", False, 2),
    Minigame(16, "N.Ballism", False, 3),
    Minigame(17, "Sky Ball", False, 4),
    Minigame(18, "Tilt Panic", False, 2),
    Minigame(19, "Polar Panic", False, 1),
    Minigame(20, "Melt Panic", False, 3),
    Minigame(21, "Manic Panic", False, 4),
    Minigame(22, "Bearminator", True, 2),
    Minigame(23, "Dot Dash", False, 3),
    Minigame(24, "Toxic Dash", False, 4),
    Minigame(25, "Splash Dash", False, 5),
    Minigame(26, "Dante's Dash", False, 5),
    Minigame(27, "Ring Ding", False, 4),
    Minigame(28, "Dragon Drop", False, 5),
    Minigame(29, "Mallet Mash", False, 5),
    Minigame(30, "Keg Kaboom", False, 5),
    Minigame(31, "Oxide Ride", True, 4)
)

id_to_minigame = {minigame.id for minigame in all_minigames}
name_to_minigame = {minigame.gameName for minigame in all_minigames}