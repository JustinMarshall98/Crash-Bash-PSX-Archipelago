import typing
from .utils import Constants

class WarpUnlock:
    id: int # Doubles as room number

    def __init__(self, _id: int):
        self.id = _id
    
    def __str__(self) -> str:
        return (
            f"Warp Room {self.id} Unlock"
        )
    
all_warp_unlocks: typing.Tuple[WarpUnlock, ...] = (
    WarpUnlock(1),
    WarpUnlock(2),
    WarpUnlock(3),
    WarpUnlock(4),
    WarpUnlock(5)
)

id_to_warp_unlock = {warpunlock.id for warpunlock in all_warp_unlocks}
name_to_warp_unlock = {str(warpunlock) for warpunlock in all_warp_unlocks}