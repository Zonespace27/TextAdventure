from ._base_test_class import TestClass
import global_textadv
from packages.verbs import *
from base_obj import new_object
from physical_obj import PhysObj
from player import Player
from packages.components.inventory import ComponentInventory
from packages.components.edible import ComponentEdible


class TestClass2(TestClass):
    def test_text_parser(self):
        self.init_things()
        self.generate_fresh_room()
        global_textadv.player_ref = Player()
        assert (global_textadv.player_ref.get_component(ComponentInventory))

        self.fresh_room.add_to_room(global_textadv.player_ref)

        apple: PhysObj = new_object(PhysObj, "apple")
        self.fresh_room.add_to_room(apple)

        global_textadv.player_ref.parse_text("pick up apple")

        assert (apple.location == global_textadv.player_ref.get_component(
            ComponentInventory))
        assert (apple.location != apple.current_room)

        global_textadv.player_ref.parse_text("eat apple")
        food_component: ComponentEdible = apple.get_component(ComponentEdible)
        assert (food_component.remaining_bites ==
                (food_component.total_bites - 1))

        global_textadv.player_ref.parse_text("eat apple")
        assert (food_component.remaining_bites ==
                (food_component.total_bites - 2))

        inventory_component: ComponentInventory = global_textadv.player_ref.get_component(
            ComponentInventory)

        global_textadv.player_ref.parse_text("eat apple")
        assert (len(inventory_component.inventory) == 0)

        global_textadv.qdel(global_textadv.player_ref)
