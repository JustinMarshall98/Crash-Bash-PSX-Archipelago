# Credit to Rosalie and her work on the FFT II project that I'm basing this on https://github.com/Rosalie-A/Archipelago/blob/finalfantasytactics/worlds/fftii/Rom.py
import json
import os
import pkgutil

import Utils

from pathlib import Path

from settings import get_settings

from .utils import Constants

import bsdiff4

from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension

from typing import BinaryIO

def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().crashbash_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(Utils.read_snes_rom(infile))
    return base_rom_bytes

class CRASHBASHPatchExtension(APPatchExtension):
    game = Constants.GAME_NAME

    @staticmethod
    def patch_rom(caller, iso, placement_file):
        patch_dict = json.loads(caller.get_file(placement_file))

        base_patch = pkgutil.get_data(__name__, "crashbashpatch.bsdiff4")
        rom_data = bsdiff4.patch(iso, base_patch)
        rom_data = bytearray(rom_data)

        # Patch the number of trophy rounds option
        rom_data[Constants.TROPHY_ROUNDS_ROM_OFFSET] = patch_dict["TrophyRounds"]

        return rom_data
    
class CRASHBASHProcedurePatch(APProcedurePatch, APTokenMixin):
    game = Constants.GAME_NAME
    hash = "637F2286B1071D42F883E5592CF2DF69"
    patch_file_ending = ".apcrashbash"
    result_file_ending = ".bin"

    procedure = [
        ("patch_rom", ["patch_file.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

    def patch(self, target: str) -> None:
        file_name = target[:-4]
        if os.path.exists(file_name + ".bin"):
            os.unlink(file_name + ".bin")
        
        super().patch(target)