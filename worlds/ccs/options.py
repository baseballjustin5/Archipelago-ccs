from dataclasses import dataclass
from Options import Toggle, Range, OptionSet, PerGameCommonOptions

class EnableTraps(Toggle):
    display_name = "Enable Traps?"
    default = False

class TrapDensity(Range):
    display_name = "Trap Desnity"
    range_start = 0
    range_end = 100
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