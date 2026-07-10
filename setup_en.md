# Crash Bash Setup Guide

## Playing Crash Bash in the Multiworld
- Play only in Adventure Mode! Do not enter a Battle or Tournament.
- Single Player and Two Player are both valid options.

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Please use version 0.4.4 or later for integrated
BizHawk support.
- Crash Bash .BIN rom.
- Make sure to launch a "New Game" for each seed you play.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later. Other emulators are not supported.
- The latest `crashbash.apworld` file. You can find this on the [Releases page](https://github.com/JustinMarshall98/Crash-Bash-PSX-Archipelago/releases). Put this in your `Archipelago/lib/worlds` folder.

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9 or greater, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open any Playstation game in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, it's because you need to load a game first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.

## Generating a Game

1. Create your options file (YAML). After installing the `crashbash.apworld` file, you can generate a template within the Archipelago Launcher by clicking `Generate Template Settings`.
2. Follow the general Archipelago instructions for [generating a game](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game).
3. Open `ArchipelagoLauncher.exe`
4. Select "Open Patch" in the right-side column. On your first time opening a patch for this game, you will also be asked to
locate `EmuHawk.exe` in your BizHawk install and your Crash Bash rom.
5. Select your patch from the generated output or downloaded from the Archipelago site from the hosted game room.

## Connecting to a Server

(Selecting Open Patch each time should do steps 1-5 for you)

1. If EmuHawk didn't launch automatically, open it manually.
2. Open your Crash Bash .bin file in EmuHawk.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing. Be careful to avoid clicking "TAStudio" below it in the menu, as this is known to delete your savefile.
4. In the Lua Console window, go to `Script > Open Script…`.
5. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator and client will eventually connect to each other. The BizHawk Client window should indicate that it
connected and recognized Crash Bash after the playstation boot logo disappears.
7. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

## Notes and Limitations

1. Items are all remote, meaning you won't receive anything for completing a challenge until you connect or reconnect
to the client. It is still safe to make progress in the game while disconnected.
2. There are some minigame requirements that are not stated in game, the option to play the games just won't appear.
I will list them here:
Jungle Fox / Metal Fox - Requires the Warp Room 2 Unlock item
Toxic Dash - Requires the Warp Room 3 Unlock item
3. Gold Relics and Gold Relic challenges will not appear in your pause menu or as options to face in the minigames until
you have entered Warp Room 4 (Forest) at least once. Logic accounts for this.
4. As noted in the yaml, the Platinum Relics option is currently always off even if you try and turn it on.
5. Entering Warp Room 5 for the first time will run the credits sequence once per save file. You can fast forward through it and continue as normal after!