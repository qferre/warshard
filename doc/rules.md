# WarShard rules

Simple wargaming rules for WW2 and later.
Designed to be easy to implement in a simulator for AI training.


Played on a hexagonal map where each hexagon is roughly 10 km and each pawn is roughly a brigade, but this can vary wildly in size depending on scale and timescale.

## Pawns

Each unit occupies a map hexagon. Several units cannot stack on the same hexagon.
Units are either Melee units or Support units.
They also have a designation ID.


| **Name**   | **Type** | **Power** | **Defense** | **Mobility** | **Range** | **Special**      |
|------------|----------|-----------|-------------|--------------|-----------|------------------|
| Infantry   | Melee    | 1         | 2           | 2            | -         |                  |
| Mechanised | Melee    | 3         | 3           | 4            | -         |                  |
| Armor      | Melee    | 6         | 3           | 6            | -         |                  |
| Artillery  | Support  | 3         | 0           | 2            | 3         |                  |
| Air wing   | Support  | 2         | 0           | 9            | 9         |                  |
| HQ         | Support  | -         | 0           | 2            | -         | Generates supply |

All Support Units have a defensive strength of 0. As such, if attacked in melee and not supported by other Support, they will be instantly destroyed.

For support units, Range is the maximum range at which they can support an attack or defence Fight, thus applying their Power value to it (see Combat).

## Turn sequence

Each side alternates, Blue then Red. Until the turn limit of the scenario is reached.

During a turn :

1) Movement phase

2) Combat Allocation phase

- The attacker specifies which units will attack which hexes. Each attacked hex is called a Fight.
- Then, in a second time, the attacker also allocates Support units.
- Finally, the defender allocates its own Support units, but cannot allocate additional melee units as defenders units (this will be represented by counterattacks in the defender’s own turn)

Note that units (including support) can only be allocated to one Fight per turn.

3) Combat Resolution phase
- For each Fight, total the combat strength of the involved Units, then roll 1d6.
- Outcomes are all applied at the same time (meaning retreating units will not contribute to another fight).

4) Upkeep phase
- For each Fight won (meaning the hex is now vacant) the attacker may pick an unit among the units involved and move it here.
- Scripted events if applicable.

## Movement

This is quite straightforward. Each unit may move up to its mobility value in number of hexes (staying in place is obviously possible) each turn.

Zone of Control: any hex adjacent to an enemy unit is in its ZoC. Entering a ZoC hex immediately ends your movement (unless you are a special unit).

### Retreats

Retreats are forced by certain combat results (see later in combat resolution table).

If there are several valid hexes for retreat, the enemy chooses the direction in which your units retreat.

One cannot retreat through enemy ZoC (even if the hex that is in enemy ZoC is already occupied by a friendly ? yes for now ?) or across impassable terrain (like a river). A unit that has to retreat but has no valid hexes to do so is destroyed.

You can stack units during a retreat, but you must correct this during your next movement phase (if you cannot correct all stackings by the end of the next movement phase, the unit with the lowest power is destroyed with ties broken randomly).


### Terrain

Normal plains cost x1 movement.

Forest, cities, or rough terrain (trench, hills) cost x2 movement, and give x2 to defender combat power.
Roads cost x0,5 movement.

Water (incl. rivers) block movement unless on bridge or for special units.


## Combat

Melee units (meaning, not support elements) can only attack adjacent hexes.

|       | **1-2** | **1-1** | **2-1** | **3-1** | **4-1** | **5-1** | **+ 6-1** |
|-------|---------|---------|---------|---------|---------|---------|-----------|
| **1** | dr      | dr      | dr      | DE      | DE      | DE      | DE        |
| **2** | S       | dr      | dr      | dr      | dr      | DE      | DE        |
| **3** | ar      | S       | dr      | dr      | dr      | dr      | DE        |
| **4** | ar      | ar      | dr      | dr      | dr      | dr      | dr        |
| **5** | ar      | ar      | ar      | dr      | EX      | EX      | dr        |
| **6** | AE      | ar      | ar      | EX      | EX      | EX      | EX        |

Outcome depending on 1d6 dice roll and strength ratio (in that order : attacker-defender). Attacking units (and support) contribute their Power. The unit being attack contributes its Defence, not its Power.

Attacks are not allowed below a 1-2 ratio in favour of the defender. Round numbers in favour of defender.

The attacker must commit at least one melee unit to each Fight. Otherwise, automatically get an "S" result (nothing happens).

Meanings:
- DR: the defending melee unit retreats by one hexagon.
- AR: all attacking melee units retreat by one hexagon.
- EX: the defender’s unit that was in the Fight hexagon is eliminated, and the attacker loses its weakest-power involved unit (ties broken at random). (maybe give attacker the choice of unit to lose ?)
- DE: all defending units, including support, are eliminated.
- AE: all attacking units, including support, are eliminated.
- S : nothing happens.

Recall that defensible terrain, like town, trenches, forest, etc. gives x2 to combat power for the melee unit of the defender.

### Supply

Units are out of supply if more than 6 hexes away from HQ. Supply lines cannot be traced through enemy ZoC.

If the defender melee unit is out of supply, add one to the attacker/defender ratio (in effect this moves one column in favour of the attacker) during combat resolution. If ANY attacker melee unit is out of supply, do the same in favor of the defender.

## Special rules and events

Some events may happen. Most common one is to bring reinforcements on certain hexes at a certain turn. In the code, I think only reinforcements will be implemented ? TODO ensure they are implemented.

Special rules depend on scenario. Not implemented in code, but could be used in a paper version, or you can enforce them yourself using the debug functions ("force_*")

Victory : some locations give victory score.

Scenario lasts a predefined number of turns.
