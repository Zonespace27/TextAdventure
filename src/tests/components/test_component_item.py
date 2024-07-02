from .._base_test_class import TestClass
import global_textadv
from packages.verbs import *
from base_obj import new_object
from physical_obj import PhysObj
from player import Player
from packages.components.inventory import ComponentInventory
from packages.components.item import ComponentItem


class TestClass2(TestClass):
    def test_item_component(self):
        self.init_things()
        self.generate_fresh_room()
        global_textadv.player_ref = new_object(Player)
        self.fresh_room.add_to_room(global_textadv.player_ref)
        item: PhysObj = new_object(PhysObj, "debug_item_2")
        # inventory_component: ComponentInventory = global_textadv.player_ref.get_component(
        #    ComponentInventory)
        item_component: ComponentItem = item.get_component(ComponentItem)
        self.fresh_room.add_to_room(item)
        item_component.unmoved_examine = "Unmoved examine text"
        # assert self.output_catcher.catch_output(
        #    global_textadv.player_ref.parse_text, ["examine item"], f"{item_component.unmoved_examine}")
        assert self.output_catcher.catch_output(
            global_textadv.player_ref.parse_text, ["pick up item"], f"You pick up the {item.name}.")
        assert self.output_catcher.catch_output(
            global_textadv.player_ref.parse_text, ["drop item"], f"You drop the {item.name}.")
        # assert self.output_catcher.catch_output(
        #    global_textadv.player_ref.parse_text, ["examine item"], "")
