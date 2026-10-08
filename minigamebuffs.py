import typing
from .utils import Constants

class MinigameBuff:
    id: int
    gameType: str

    def __init__(self, _id: int, _gameType: str):
        self.id = _id
        self.gameType = _gameType
    
    def __str__(self) -> str:
        return (
            f"Progressive {self.gameType} Buff"
        )
    
all_minigame_buffs: typing.Tuple[MinigameBuff, ...] = (
    MinigameBuff(0, "Ballistix"),
    MinigameBuff(1, "Crate Crush"),
    MinigameBuff(2, "Polar Push"),
    MinigameBuff(3, "Pogo Pandemonium"),
    MinigameBuff(4, "Tank Wars"),
    MinigameBuff(5, "Crash Dash"),
    MinigameBuff(6, "Medieval Mayhem"),
    MinigameBuff(7, "Bosses")

)

id_to_minigame_buff = {minigamebuff.id for minigamebuff in all_minigame_buffs}
name_to_minigame_buff = {str(minigamebuff) for minigamebuff in all_minigame_buffs}