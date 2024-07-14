from .._base_test_class import TestClass
import global_textadv
from packages.verbs import *
from base_obj import new_object
from player import Player
from packages.components.laying_down import ComponentLayingDown


class TestClass2(TestClass):
    def test_laying_down_component(self):
        self.init_things()
        self.generate_fresh_room()
        global_textadv.player_ref = new_object(Player)
        self.fresh_room.add_to_room(global_textadv.player_ref)
        global_textadv.player_ref.add_component(ComponentLayingDown, {})
        laying_component: ComponentLayingDown = global_textadv.player_ref.get_component(
            ComponentLayingDown)
        assert self.output_catcher.catch_output(
            global_textadv.player_ref.parse_text, ["check inventory"], laying_component.block_interaction_message)
        assert self.output_catcher.catch_output(
            global_textadv.player_ref.parse_text, ["get up"], laying_component.get_up_message)
        assert not global_textadv.player_ref.get_component(ComponentLayingDown)
