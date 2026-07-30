from test.bases import WorldTestBase
from worlds.ccs.items import ITEM_TABLE


class CcsTest(WorldTestBase):
    game = "Cash cleaner simulator"

    def test_locations_and_items_present(self):
        # Ensure locations are present and itempool size matches the ITEM_TABLE
        self.assertEqual(len(list(self.multiworld.get_locations())), 3)
        self.assertEqual(len(self.multiworld.itempool), len(ITEM_TABLE))

    def test_beatable_when_all_items_collected(self):
        # Collect one item per unique item name and assert the game is beatable
        unique_names = set(self.multiworld.item_name_to_id.keys())
        collected = []
        for name in unique_names:
            items = self.get_items_by_name([name])
            if items:
                collected.append(items[0])
        self.collect(collected)
        self.assertTrue(self.multiworld.can_beat_game(self.multiworld.state))
