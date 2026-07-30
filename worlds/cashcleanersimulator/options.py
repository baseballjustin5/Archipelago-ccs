from dataclasses import dataclass
from Options import Toggle, Range, OptionSet, PerGameCommonOptions, Choice

class EnableTraps(Toggle):
    display_name = "Enable Traps?"
    default = False

class GameLength(Choice):
    display_name = "Game Length"
    option_short = 20
    option_medium = 43
    option_long = 65
    default = 25

class TrapDensity(Range):
    display_name = "Trap Density"
    option_low = 5
    option_medium = 10
    option_high = 15
    range_start = 0
    range_end = 20
    default = 10

class Traps(OptionSet):
    display_name = "Enabled Trap Types"
    valid_keys = {"Trash Items", "Wet Bills", "Dirty Bills", "Inked Bills", "Goo Bills", "All"}
    default = {"All"}

@dataclass
class CashCleanerSimulatorOptions(PerGameCommonOptions):
    enable_traps: EnableTraps
    trap_density: TrapDensity
    selected_traps: Traps
    game_length: GameLength