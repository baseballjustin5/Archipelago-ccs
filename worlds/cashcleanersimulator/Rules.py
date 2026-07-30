"""
Access rules for Cash cleaner simulator (ccs).

This module defines capability predicates (washer/dryer/money/marked/goo detection ...)
and applies them to locations.
"""
from __future__ import annotations

from typing import Callable

from worlds.generic.Rules import add_rule, set_rule, location_item_name

BASE_REP_NEED = [32, 24, 16, 8]
HIGH_REP_NEED = [40, 32, 24, 16]
LOW_REP_NEED = [24, 16, 8, 1]


def reputation_at_least(player, amount: int) -> Callable:
    return lambda state: state.has("Reputation", player, amount - 1)

def has_done_quest(player, quest) -> Callable:
    return lambda state: state.has(quest + " completed", player)

def has_opened_upper_area(player) -> Callable:
    return lambda state: state.has("Unlock upper area" + " completed", player)

def has_opened_relax_area(player) -> Callable:
    return lambda state: state.has("Unlock relax area" + " completed", player)

def has_workbench_access(player) -> Callable:
    return lambda state: has_done_quest(player, "Main Quest Side: Hot Dry")(state)

def has_access(player, item, rep_need) -> Callable:
    return lambda state: reputation_at_least(player, rep_need[state.count(item, player)])(state)

def has_washer(player) -> Callable:
    return lambda state: has_access(player, "Reduced Washer requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced Big Washer requirement", HIGH_REP_NEED)(state) or (has_workbench_access(player)(state) and has_access(player, "Reduced Sponge requirement", BASE_REP_NEED)(state)) or has_opened_upper_area(player)(state)

def has_dryer(player) -> Callable:
    return lambda state: has_access(player, "Reduced Dryer requirement", BASE_REP_NEED)(state)

def has_fake_money_detector(player) -> Callable:
    return lambda state: has_workbench_access(player)(state) or has_access(player, "Reduced Money counter tier 2 requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced Euro Money counter tier 2 requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced Yen Money counter tier 2 requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced Money counter tier 3 requirement", HIGH_REP_NEED)(state) or has_access(player, "Reduced UV Lamp requirement", BASE_REP_NEED)(state)

def has_marked_detector(player) -> Callable:
    return lambda state: has_workbench_access(player)(state) or has_access(player, "Reduced Marked money Counter requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced UV Lamp requirement", BASE_REP_NEED)(state)

def has_degoo(player) -> Callable:
    return lambda state: (has_workbench_access(player)(state) and has_access(player, "Reduced Goo detergent requirement", HIGH_REP_NEED)(state)) or ((has_access(player, "Reduced Big Washer requirement", HIGH_REP_NEED)(state) or has_opened_upper_area(player)(state)) and has_access(player, "Reduced Goo detergent requirement", HIGH_REP_NEED)(state))

def has_deink(player) -> Callable:
    return lambda state: (has_workbench_access(player)(state) and has_access(player, "Reduced Workbench Ink Foam requirement", LOW_REP_NEED)(state)) or ((has_access(player, "Reduced Big Washer requirement", HIGH_REP_NEED)(state) or has_opened_upper_area(player)(state)) and has_access(player, "Reduced Ink detergent requirement", LOW_REP_NEED)(state))

def has_sticker(player) -> Callable:
    return lambda state: has_access(player, "Reduced Sticker gun requirement", BASE_REP_NEED)(state)

def has_moneygun(player) -> Callable:
    return lambda state: has_access(player, "Reduced Money gun requirement", BASE_REP_NEED)(state)

def has_ladder(player) -> Callable:
    return lambda state: has_access(player, "Reduced Ladder requirement", LOW_REP_NEED)(state)

def has_counter(player) -> Callable:
    return lambda state: has_access(player, "Reduced Money counter requirement", LOW_REP_NEED)(state) or has_access(player, "Reduced Money counter tier 2 requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced Euro Money counter tier 2 requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced Yen Money counter tier 2 requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced Money counter tier 3 requirement", HIGH_REP_NEED)(state) or has_access(player, "Reduced UV Lamp requirement", BASE_REP_NEED)(state)

def has_euro_counter(player) -> Callable:
    return lambda state: has_access(player, "Reduced Euro Money counter tier 2 requirement", BASE_REP_NEED)(state) or has_access(player, "Reduced Money counter tier 3 requirement", HIGH_REP_NEED)(state)

def has_all_denomination_counter(player) -> Callable:
    return lambda state: (has_access(player, "Reduced Money counter tier 2 requirement", BASE_REP_NEED)(state) and has_access(player, "Reduced Euro Money counter tier 2 requirement", BASE_REP_NEED)(state) and has_access(player, "Reduced Yen Money counter tier 2 requirement", BASE_REP_NEED)(state)) or has_access(player, "Reduced Money counter tier 3 requirement", HIGH_REP_NEED)(state)

location_name_to_rule = {
    "Main Quest Tutorial: Controls Movement":       lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Tutorial: Controls Interactions":   lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Tutorial: Smartphone":              lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Tutorial: Manipulation":            lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Tutorial: Conveyor":                lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Side: The Call Of Cash":            lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Tutorial: Take Quest":              lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Tutorial: Task Tracker":            lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Tutorial: Finish Quest":            lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Main: Clean It Or Skip It":         lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Main Quest Main: Shop Till It Drops":          lambda player: lambda state: reputation_at_least(player, 1)(state) and has_access(player, "Reduced Money counter requirement", LOW_REP_NEED)(state),
    "Main Quest Side: The Wet Case":                lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Main: Clean It Or Skip It")(state),
    "Main Quest Side: Fifty Shades Of Cash":        lambda player: lambda state: reputation_at_least(player, 2)(state) and has_done_quest(player, "Main Quest Side: The Wet Case")(state),
    "Main Quest Side: Hot Dry":                     lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Side: Fifty Shades Of Cash")(state),
    "Main Quest Side: Clean Cut":                   lambda player: lambda state: reputation_at_least(player, 2)(state) and has_done_quest(player, "Main Quest Side: Hot Dry")(state) and has_washer(player)(state),
    "Main Quest Side: Two Cases":                   lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Side: Clean Cut")(state) and has_washer(player)(state),
    "Main Quest Side: From Chaos To Cash":          lambda player: lambda state: reputation_at_least(player, 3)(state) and has_done_quest(player, "Main Quest Side: Two Cases")(state),
    "Main Quest Side: Silent Deal":                 lambda player: lambda state: reputation_at_least(player, 2)(state) and has_done_quest(player, "Main Quest Side: Two Cases")(state),
    "Main Quest Side: Fake Fluff":                  lambda player: lambda state: reputation_at_least(player, 4)(state) and has_done_quest(player, "Main Quest Side: Silent Deal")(state) and has_fake_money_detector(player)(state),
    "Main Quest Side: No Stains":                   lambda player: lambda state: reputation_at_least(player, 2)(state) and has_done_quest(player, "Main Quest Side: From Chaos To Cash")(state) and has_marked_detector(player)(state),
    "Main Quest Main: Cleansing Fire":              lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Side: Hot Dry")(state),
    "Main Quest Main: The Light Test":              lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Side: Clean Cut")(state) and has_fake_money_detector(player)(state),
    "Main Quest Side: Light It Up":                 lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Main: The Light Test")(state) and has_ladder(player)(state),
    "Main Quest Main: Feed The Pig":                lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Main Quest Side: Different Values":            lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Main Quest Main: Europhoria":                  lambda player: lambda state: reputation_at_least(player, 8)(state) and has_done_quest(player, "Main Quest Main: Feed The Pig")(state) and has_euro_counter(player)(state),
    "Main Quest Main: Blacklight Evidence":         lambda player: lambda state: reputation_at_least(player, 9)(state) and has_done_quest(player, "Main Quest Main: Europhoria")(state) and has_marked_detector(player)(state),
    "Main Quest Main: Pre Launch Protocol":         lambda player: lambda state: reputation_at_least(player, 10)(state) and has_opened_upper_area(player)(state),
    "Main Quest Main: Saving Piglet":               lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Main: Blacklight Evidence")(state),
    "Main Quest Side: Luxury Wrapping":             lambda player: lambda state: reputation_at_least(player, 9)(state) and has_done_quest(player, "Main Quest Side: Different Values")(state),
    "Main Quest Main: Golden Cage Breakout":        lambda player: lambda state: reputation_at_least(player, 11)(state) and has_done_quest(player, "Main Quest Main: Saving Piglet")(state) and has_euro_counter(player)(state),
    "Main Quest Side: Fragile Treasure":            lambda player: lambda state: reputation_at_least(player, 8)(state) and has_done_quest(player, "Main Quest Side: Luxury Wrapping")(state) and has_washer(player)(state) and has_dryer(player)(state),
    "Main Quest Side: Financial Exorcism":          lambda player: lambda state: reputation_at_least(player, 9)(state) and has_done_quest(player, "Main Quest Side: Fragile Treasure")(state) and has_washer(player)(state) and has_dryer(player)(state) and has_marked_detector(player)(state),
    "Main Quest Side: What They Left Behind":       lambda player: lambda state: reputation_at_least(player, 8)(state) and has_done_quest(player, "Main Quest Side: Financial Exorcism")(state),
    "Main Quest Side: Financial Zoo":               lambda player: lambda state: reputation_at_least(player, 11)(state) and has_done_quest(player, "Main Quest Side: What They Left Behind")(state),
    "Main Quest Side: Tracing The Bullet":          lambda player: lambda state: reputation_at_least(player, 8)(state) and has_done_quest(player, "Main Quest Side: Financial Zoo")(state),
    "Main Quest Side: Collectors Edition":          lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Side: Tracing The Bullet")(state),
    "Main Quest Side: The Money Flow":              lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Side: Collectors Edition")(state) and has_all_denomination_counter(player)(state) and has_washer(player)(state) and has_deink(player)(state),
    "Main Quest Side: The Magician Choice":         lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Side: The Money Flow")(state) and has_all_denomination_counter(player)(state) and has_washer(player)(state) and has_dryer(player)(state),
    "Main Quest Side: Ocean Of Emojis":             lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "Main Quest Side: The Magician Choice")(state) and has_washer(player)(state) and has_dryer(player)(state),
    "Main Quest Side: Lawful Goo":                  lambda player: lambda state: reputation_at_least(player, 16)(state) and has_degoo(player)(state),
    "Main Quest Side: Mind Your Business":          lambda player: lambda state: reputation_at_least(player, 21)(state),
    "Main Quest Main: The Vault Of Truth":          lambda player: lambda state: reputation_at_least(player, 11)(state) and has_done_quest(player, "Main Quest Main: Golden Cage Breakout")(state),
    "Main Quest Main: Operation Black File":        lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Main: Golden Cage Breakout")(state),
    "Main Quest Side: Combo Heist":                 lambda player: lambda state: reputation_at_least(player, 8)(state) and has_done_quest(player, "Main Quest Main: Golden Cage Breakout")(state) and has_washer(player)(state) and has_dryer(player)(state),
    "Main Quest Main: Launch Code OINK":            lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Main: The Vault Of Truth")(state) and has_opened_upper_area(player)(state),
    "Main Quest Main: Inflation Sequence":          lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Main: Launch Code OINK")(state) and has_opened_upper_area(player)(state),
    "Main Quest Main: Priming The Shot":            lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Main: Operation Black File")(state) and has_opened_relax_area(player)(state),
    "Main Quest Main: Loaded But Undecided":        lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Main: Priming The Shot")(state) and has_opened_relax_area(player)(state),
    "Main Quest Side: Acid Conspiracy":             lambda player: lambda state: reputation_at_least(player, 16)(state) and has_degoo(player)(state) and has_done_quest(player, "Main Quest Side: Lawful Goo")(state),
    "Main Quest Main: Final Ascent":                lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Main: Inflation Sequence")(state) and has_opened_upper_area(player)(state),
    "Main Quest Main: Point Of No Return":          lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "Main Quest Main: Loaded But Undecided")(state) and has_opened_relax_area(player)(state),
    # Side quests
    "SideQuest 1":                                  lambda player: lambda state: reputation_at_least(player, 1)(state),
    "SideQuest 2":                                  lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 1")(state),
    "SideQuest 3":                                  lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 2")(state),
    "SideQuest 4":                                  lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 3")(state),
    "SideQuest 5":                                  lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 4")(state),
    "SideQuest 6":                                  lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 5")(state),
    "SideQuest 7":                                  lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 6")(state),
    "SideQuest 8":                                  lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 7")(state),
    "SideQuest 9":                                  lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 8")(state),
    "SideQuest 10":                                 lambda player: lambda state: reputation_at_least(player, 1)(state) and has_done_quest(player, "SideQuest 9")(state),
    "SideQuest 11":                                 lambda player: lambda state: reputation_at_least(player, 5)(state) and has_done_quest(player, "SideQuest 10")(state),
    "SideQuest 12":                                 lambda player: lambda state: reputation_at_least(player, 5)(state) and has_done_quest(player, "SideQuest 11")(state),
    "SideQuest 13":                                 lambda player: lambda state: reputation_at_least(player, 5)(state) and has_done_quest(player, "SideQuest 12")(state),
    "SideQuest 14":                                 lambda player: lambda state: reputation_at_least(player, 5)(state) and has_done_quest(player, "SideQuest 13")(state),
    "SideQuest 15":                                 lambda player: lambda state: reputation_at_least(player, 5)(state) and has_done_quest(player, "SideQuest 14")(state),
    "SideQuest 16":                                 lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "SideQuest 15")(state) and has_counter(player)(state),
    "SideQuest 17":                                 lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "SideQuest 16")(state) and has_counter(player)(state),
    "SideQuest 18":                                 lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "SideQuest 17")(state) and has_counter(player)(state),
    "SideQuest 19":                                 lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "SideQuest 18")(state) and has_counter(player)(state),
    "SideQuest 20":                                 lambda player: lambda state: reputation_at_least(player, 10)(state) and has_done_quest(player, "SideQuest 19")(state) and has_counter(player)(state),
    "SideQuest 21":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 20")(state) and has_counter(player)(state),
    "SideQuest 22":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 21")(state) and has_counter(player)(state),
    "SideQuest 23":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 22")(state) and has_counter(player)(state),
    "SideQuest 24":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 23")(state) and has_counter(player)(state),
    "SideQuest 25":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 24")(state) and has_counter(player)(state),
    "SideQuest 26":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 25")(state) and has_counter(player)(state),
    "SideQuest 27":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 26")(state) and has_counter(player)(state),
    "SideQuest 28":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 27")(state) and has_counter(player)(state),
    "SideQuest 29":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 28")(state) and has_counter(player)(state),
    "SideQuest 30":                                 lambda player: lambda state: reputation_at_least(player, 15)(state) and has_done_quest(player, "SideQuest 29")(state) and has_counter(player)(state),
    # Side quests bonus
    "Quest Bonus: Exact money value":               lambda player: lambda state: state.has("Main Quest Tutorial: Conveyor completed", player),
    "Quest Bonus: More money value":                lambda player: lambda state: state.has("Main Quest Tutorial: Conveyor completed", player),
    "Quest Bonus: Much more money value":           lambda player: lambda state: state.has("Main Quest Tutorial: Conveyor completed", player),
    "Quest Bonus: Single delivery":                 lambda player: lambda state: reputation_at_least(player, 2)(state),
    "Quest Bonus: Nothing else":                    lambda player: lambda state: reputation_at_least(player, 2)(state),
    "Quest Bonus: No marked money":                 lambda player: lambda state: has_marked_detector(player)(state),
    "Quest Bonus: No marked money specific quest":  lambda player: lambda state: has_marked_detector(player)(state) and reputation_at_least(player, 6)(state),
    "Quest Bonus: No fake money":                   lambda player: lambda state: has_fake_money_detector(player)(state),
    "Quest Bonus: No fake money specific quest":    lambda player: lambda state: has_fake_money_detector(player)(state) and reputation_at_least(player, 6)(state),
    "Quest Bonus: Perfect packs":                   lambda player: lambda state: reputation_at_least(player, 2)(state),
    "Quest Bonus: Perfect packs specific quest":    lambda player: lambda state: reputation_at_least(player, 2)(state),
    "Quest Bonus: Perfect blocks":                  lambda player: lambda state: reputation_at_least(player, 2)(state),
    "Quest Bonus: Perfect blocks specific quest":   lambda player: lambda state: reputation_at_least(player, 2)(state),
    "Quest Bonus: Marked with Labels!":             lambda player: lambda state: has_sticker(player)(state),
    "Quest Bonus: Perfect rolls":                   lambda player: lambda state: reputation_at_least(player, 2)(state),
    "Quest Bonus: Perfect roll-blocks":             lambda player: lambda state: reputation_at_least(player, 2)(state),
    # World interactions
    "Unlock relax area":                            lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state) and reputation_at_least(player, 9)(state),
    "Unlock upper area":                            lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state) and reputation_at_least(player, 9)(state),
    "Dunk!":                                        lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Rest out of bound":                            lambda player: lambda state: has_ladder(player)(state),
    "Buy a money gun":                              lambda player: lambda state: has_moneygun(player)(state),
    "Marked bill collection: FBI":                  lambda player: lambda state: reputation_at_least(player, 6)(state) and has_marked_detector(player)(state),
    "Marked bill collection: Police":               lambda player: lambda state: reputation_at_least(player, 6)(state) and has_marked_detector(player)(state),
    "Marked bill collection: Yakuza":               lambda player: lambda state: reputation_at_least(player, 6)(state) and has_marked_detector(player)(state),
    "Marked bill collection: Mafia":                lambda player: lambda state: reputation_at_least(player, 6)(state) and has_marked_detector(player)(state),
    "Marked bill collection: Cartel":               lambda player: lambda state: reputation_at_least(player, 6)(state) and has_marked_detector(player)(state),
    "Marked bill collection: Unknown":              lambda player: lambda state: reputation_at_least(player, 6)(state) and has_marked_detector(player)(state),
    "Coin collection: Pitcoin":                     lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Coin collection: Legionnare":                  lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Coin collection: Liberty":                     lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Coin collection: Pirate":                      lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Coin collection: Ashoka Lion":                 lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Coin collection: Fugio":                       lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Coin collection: Edokoban":                    lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Coin collection: Retro Pixel":                 lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Art Bill collection: EUR 100":                 lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: EUR 50":                  lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: EUR 20":                  lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: JPY 10000":               lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: JPY 5000":                lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: JPY 1000":                lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: USD 100":                 lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: USD 50":                  lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: USD 20":                  lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    "Art Bill collection: USD 10":                  lambda player: lambda state: has_done_quest(player, "Main Quest Side: Light It Up")(state),
    # SideQuest Difficulty
    "Side quest Difficulty 0":                      lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Side quest Difficulty 1":                      lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Side quest Difficulty 2":                      lambda player: lambda state: reputation_at_least(player, 1)(state),
    "Side quest Difficulty 3":                      lambda player: lambda state: reputation_at_least(player, 4)(state) and has_counter(player)(state),
    "Side quest Difficulty 4":                      lambda player: lambda state: reputation_at_least(player, 8)(state) and has_counter(player)(state),
    "Side quest Difficulty 5":                      lambda player: lambda state: reputation_at_least(player, 14)(state) and has_counter(player)(state),
    "Side quest Difficulty 6":                      lambda player: lambda state: reputation_at_least(player, 22)(state) and has_counter(player)(state),
    "Side quest Difficulty 7":                      lambda player: lambda state: reputation_at_least(player, 24)(state) and has_counter(player)(state),
    "Side quest Difficulty 8":                      lambda player: lambda state: reputation_at_least(player, 34)(state) and has_counter(player)(state),
    "Side quest Difficulty 9":                      lambda player: lambda state: reputation_at_least(player, 38)(state) and has_counter(player)(state),
                                   
}



def set_rules(world) -> None:
    player = world.player
    mw = world.multiworld

    for loc_name in world.location_name_to_id.keys():
        loc = mw.get_location(loc_name, player)
        set_rule(loc, location_name_to_rule[loc_name](player))

def main_quest_rule(quest_name: str) -> Callable:
    return location_name_to_rule[quest_name]
def side_quest_rule(quest_name: str) -> Callable:
    return location_name_to_rule[quest_name]
def relax_rule() -> Callable:
    return location_name_to_rule["Unlock relax area"]
def upper_area_rule() -> Callable:
    return location_name_to_rule["Unlock upper area"]
def victory_rule() -> Callable:
    return lambda player: lambda state: has_done_quest(player, "Main Quest Main: Final Ascent")(state) or has_done_quest(player, "Main Quest Main: Point Of No Return")(state)