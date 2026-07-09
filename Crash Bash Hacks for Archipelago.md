Crash Bash Hacks for Archipelago
Hacks Authored by Jumza (unless otherwise stated)

Name: Switch between non-consecutive warp room selections
Description: In the base game if you have only (for example) warp room access to 1,2,4, you could not move your selected
warp room between 2 and 4 more than once. This enables this behaviour.
In addition, I am moving all warp checks over by 1 to move their data points off of where boss completion locations are.
New Warp Room Unlock Memory Locations - (Access to 1 is always on by default right now)
0x5A781 - Warp Room 2 Unlocked
0x5A786 - Warp Room 4 Unlocked
0x5A793 - Warp Room 3 Unlocked
0x5A79C - Warp Room 5 Unlocked

Additional implementation note: Uses space freed up in the New Locations for Trophy / Gem / Crystal / Gold Relic Amounts (Menu Counts) hack (the ending nops, after the branch)

Offset (ROM): 0x504DF88
j 0x800814F0
nop

Offset (ROM): 0x50563F8
lbu r3, 0x0169(r2)
nop
bne r3, r0, @EndCheck
lui r4, 0x800B
ori r4, 0xCEE0
lbu r2, 0x0000(r4)
ori r1,r0,0x0003
addi r2,r2,0x0001
div r2,r1
nop
mfhi r2
sb r2,0x0000(r4)
@EndCheck:
j 0x8007A254
nop



Name: Rounds Required for Trophy
Description: Modifies the number of wins required to complete a Trophy challenge. In vanilla this is 3.
Change 0x0003 to desired result.

Offset (ROM): 0x5052FFC
r6,r0,0x0003




Name: New Locations for Trophy / Gem / Crystal / Gold Relic Amounts (Challenge Checks)
Description: In the vanilla game Crash Bash iterates over all Trophy / Gem / Crystal / Relic locations for each game and sees
what you have completed. For Archipelago I want to divorce total number of these items that we have from the challenges
we have completed. So overwrite the original loop by checking our new data locations for these item counts.
Checked for entrance to various challenges (like boss requirements), pause menu count is a different routine.

New locations - Description - Output expected by Vanilla functions that use this routine
0x5A782 - Trophies Received from Multiworld - Ends up in r7
0x5A783 - Gems Received from Multiworld - Ends up in r8
0x5A784 - Crystals Received from Multiworld - Ends up in r10
0x5A787 - Gold Relics Received from Multiworld - Ends up in r9
0x5A788 - Platinum Relics Received from Multiworld (unused rn) - Not checked in vanilla

Offset (ROM): 0x504DEBC
addu r10,r0,r0
addu r9,r10,r0
addu r8,r10,r0
addu r7,r10,r0
addu r6,r10,r0
lui r2, 0x8005
ori r2,r2,0xA000
nop
lbu r7, 0x0782(r2)
lbu r8, 0x0783(r2)
lbu r10, 0x0784(r2)
lbu r9, 0x0787(r2)
nop
nop
nop
nop
nop
nop


Name: New Locations for Trophy / Gem / Crystal / Gold Relic Amounts (Menu Counts)
Description: In the vanilla game Crash Bash iterates over all Trophy / Gem / Crystal / Relic locations for each game and sees
what you have completed. For Archipelago I want to divorce total number of these items that we have from the challenges
we have completed. So overwrite the original loop by checking our new data locations for these item counts.
Checked for the count displayed on the pause menu, challenge entrance requirements is a different routine.

New locations - Description - Output expected by Vanilla functions that use this routine
0x5A782 - Trophies Received from Multiworld - Ends up in r18
0x5A783 - Gems Received from Multiworld - Ends up in r19
0x5A784 - Crystals Received from Multiworld - Ends up in r20
0x5A787 - Gold Relics Received from Multiworld - Ends up in r21
0x5A788 - Platinum Relics Received from Multiworld (unused rn) - Ends up in r22

Offset (ROM): 0x5056248
addiu r29,r29,-0x0040
sw r16,0x0020(r29)
addu r16,r4,r0
sw r20,0x0030(r29)
addu r20,r0,r0
sw r22,0x0038(r29)
addu r22,r20,r0
sw r21,0x0034(r29)

We run into what I think is a sector boundary on the disc here, we have to put the rest of the routine in afterwards.

Offset (ROM): 0x5056398
addu r21,r20,r0
sw r19,0x002c(r29)
addu r19,r20,r0
sw r18,0x0028(r29)
addu r18,r20,r0
addu r13,r20,r0
lui r2,0x8006
addiu r5,r2,-0x59ec
addiu r4,r0,0x0002
sw r31,0x003c(r29)
sw r17,0x0024(r29)
addu r3,r13,r5
lui r2, 0x8005
ori r2,r2,0xA000
nop
lbu r18, 0x0782(r2)
lbu r19, 0x0783(r2)
lbu r20, 0x0784(r2)
lbu r21, 0x0787(r2)
lbu r22, 0x0788(r2)
nop
nop
b @TrophyCheckEnd
ori r13, r0, 0x0004 # Loop counter that is checked later
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
@TrophyCheckEnd:
nop




Name: Remove LibCrypt anti-piracy
Description: Bizhawk seems to run the game fine anyway from my game dump but I'm removing it so I can test on the pSX v1.13 emulator and just because I don't like it being there :P
AUTHOR: BadHabit (thank you for posting this online for me to find!)

Offset (ROM): 0x2F696
Change 40 to 00 to remove LibCrypt check