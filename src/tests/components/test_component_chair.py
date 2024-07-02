from .._base_test_class import TestClass
import global_textadv
from main import unit_test_genesis
from packages.verbs import *
from base_obj import new_object
from physical_obj import PhysObj
from player import Player
from packages.components.chair import ComponentChair


class TestClass2(TestClass):
    def test_chair_component(self):
        self.init_things()
        self.generate_fresh_room()
        global_textadv.player_ref = new_object(Player)
        self.fresh_room.add_to_room(global_textadv.player_ref)
        chair: PhysObj = new_object(PhysObj, "reception_chair")
        chair_component: ComponentChair = chair.get_component(ComponentChair)
        self.fresh_room.add_to_room(chair)
        assert self.output_catcher.catch_output(
            global_textadv.player_ref.parse_text, ["sit in chair"], chair_component.sit_down_message)
        assert self.output_catcher.catch_output(
            global_textadv.player_ref.parse_text, ["get up from chair"], chair_component.get_up_message)
