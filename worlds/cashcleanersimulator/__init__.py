"""
Minimal Cash Cleaner Simulator world for Archipelago

This is a minimal, example implementation to get a new world into the generator.
Add TODOs for any missing game-specific logic (regions, locations, items, rules).
"""
from typing import ClassVar, Dict, cast
import zipfile
import os

from BaseClasses import Item, ItemClassification, Location, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

from . import items as _items
from . import locations as _locations
from .Rules import main_quest_rule, relax_rule, set_rules as set_ccs_rules, side_quest_rule, upper_area_rule, victory_rule
from .options import CashCleanerSimulatorOptions



class CcsLocation(Location):
    game: str = "Cash Cleaner Simulator"

class CcsItem(Item):
    game: str = "Cash Cleaner Simulator"

class CcsWebWorld(WebWorld):
    theme = "default"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A short setup guide for Cash Cleaner Simulator.",
            "English",
            "setup_en.md",
            "setup/en",
            ["YourName"],
        )
    ]


class CcsWorld(World):
    """
    Minimal Cash Cleaner Simulator world.

    TODOs:
      - Add accurate regions and locations
      - Flesh out items and item behaviours
      - Add options and presets if desired
    """
    game: str = "Cash Cleaner Simulator"
    web = CcsWebWorld()

    options_dataclass = CashCleanerSimulatorOptions

    # ID maps are loaded from `worlds/ccs/items.py` and `worlds/ccs/locations.py`,
    # which attempt to read `rewardList.lua` and `rewardLocations.lua` if present.
    item_name_to_id: ClassVar[Dict[str, int]] = _items.item_name_to_id
    location_name_to_id: ClassVar[Dict[str, int]] = _locations.location_name_to_id

    def generate_early(self) -> None:
        """ Set up the itempool for generation. """
        opts = cast(CashCleanerSimulatorOptions, self.options)
        enable_traps = opts.enable_traps.value
        trap_density = opts.trap_density.value
        selected_traps = opts.selected_traps.value

        # 20 (Short), 25 (Default), 43 (Medium), 65 (Long)
        game_length = opts.game_length.value 

        item_counts = dict(_items.item_name_to_count)

        base_rep_count = 15
        filler_rep_count = max(0, (game_length - base_rep_count))

        item_counts["Reputation"] = base_rep_count
        item_counts["Filler Reputation"] = filler_rep_count

        """
        TODO: determine realistic item counts and pre-placed items.
        """
        # Populate the itempool by preserving multiplicity from ITEM_TABLE (one Item per table entry)
        itempool = []
        for name, count in _items.item_name_to_count.items():
            item_id = self.item_name_to_id[name]
            classification = _items.item_name_to_classification[name]
            for _ in range(count):
                itempool.append(
                    CcsItem(
                        name,
                        classification,
                        item_id,
                        self.player,
                    )
                )

        total_locations = len(self.location_name_to_id)
        filler_needed = total_locations - len(itempool)
    
        if enable_traps and filler_needed > 0:
            import math
            num_traps = math.floor(filler_needed * (trap_density/100))

            if "All" in selected_traps:
                active_trap_types = ["Trash Items", "Wet Bills", "Dirty Bills", "Inked Bills", "Goo Bills"]
            else:
                active_trap_types = list(selected_traps)

            if active_trap_types and num_traps > 0:
                for i in range(num_traps):
                    trap_name = active_trap_types[i % len(active_trap_types)]
                    trap_id = self.item_name_to_id.get(trap_name)

                    if trap_id is not None:
                        itempool.append(
                            CcsItem(
                                trap_name,
                                ItemClassification.trap,
                                trap_id,
                                self.player,
                            )
                        )

        self.multiworld.itempool += itempool
        self.precollected = []

    def set_rules(self) -> None:
        # Apply world-specific access rules
        set_ccs_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_event_location(self, region, location_name, rule, item: str):
        region = self.multiworld.get_region(region, self.player)
        region.add_event(location_name, item, rule, CcsLocation, CcsItem)

    def create_regions(self) -> None:
        """Create a single origin region and attach minimal locations."""
        player = self.player
        mw = self.multiworld

        origin = Region("Menu", player, mw, hint="Start")
        mw.regions.append(origin)

        # Create and append locations
        for loc_name in self.location_name_to_id.keys():
            origin.add_locations({ loc_name: self.location_name_to_id[loc_name] })
            if loc_name.startswith("Main Quest"):
                self.create_event_location("Menu", loc_name + " completed", main_quest_rule(loc_name)(player), loc_name + " completed")
            if loc_name.startswith("SideQuest"):
                self.create_event_location("Menu", loc_name + " completed", side_quest_rule(loc_name)(player), loc_name + " completed")
            if loc_name == "Unlock relax area":
                self.create_event_location("Menu", loc_name + " completed", relax_rule()(player), loc_name + " completed")
            if loc_name == "Unlock upper area":
                self.create_event_location("Menu", loc_name + " completed", upper_area_rule()(player), loc_name + " completed")
           
        self.create_event_location("Menu", "Victory", victory_rule()(player), "Victory")

        
    def create_item(self, name: str) -> Item:
        """
        Return an Item instance for the given item name.
        """
        
        code = self.item_name_to_id.get(name)
        classification = _items.item_name_to_classification[name]
        # default all items to progression for minimal behavior; adjust as needed

        return CcsItem(name, classification, code, self.player)

    def generate_output(self, output_directory: str):
        player_name = self.multiworld.player_name[self.player]
        player_name = player_name.replace("\\", "\\\\").replace('"', '\\"')
        
        zip_name = f"{player_name}_ccs_ap_config.zip"
        zip_path = os.path.join(output_directory, zip_name)

        lua_filename = "ap_config.lua"

        lua_content = (
            "return {\n"
            '    host = "",\n'
            f'    player = "{player_name}",\n'
            '    password = "",\n'
            f'    seed = {self.multiworld.seed},\n'
            "}\n"
        )

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr(lua_filename, lua_content)