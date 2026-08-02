from dataclasses import dataclass
from Options import Toggle, Range, OptionSet, PerGameCommonOptions, Choice

class EnableTraps(Toggle):
    """ Enable or disable traps from appearing in your world's item pool.
    Options: True or False"""
    display_name = "Enable Traps?"
    default = False

class GameLength(Choice):
    """
    Controls the overall length of the seed and the expected item pool scaling.
    option_short = 65 Reputaion level up items added to pool
    option_medium = 43 Reputaion level up items added to pool
    option_long = 34 Reputaion level up items added to pool
    """
    display_name = "Game Length"
    option_short = 65
    option_medium = 43
    option_long = 34
    default = 43

class TrapDensity(Range):
    """ What % of traps are swapped for filler items."""
    display_name = "Trap Density"
    option_low = 5
    option_medium = 10
    option_high = 15
    range_start = 0
    range_end = 20
    default = 10

class Traps(OptionSet):
    """Select which specific types of traps are allowed to spawn in your multiworld.
    Available options: 'Trash Items', 'Wet Bills', 'Dirty Bills', 'Inked Bills', 'Goo Bills', or 'All'"""
    display_name = "Enabled Trap Types"
    valid_keys = {"Trash Items", "Wet Bills", "Dirty Bills", "Inked Bills", "Goo Bills", "All"}
    default = {"All"}

@dataclass
class CashCleanerSimulatorOptions(PerGameCommonOptions):
    enable_traps: EnableTraps
    trap_density: TrapDensity
    selected_traps: Traps
    game_length: GameLength
