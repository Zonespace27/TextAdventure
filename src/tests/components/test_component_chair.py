from room import Room
import global_textadv
from main import unit_test_genesis
from packages.verbs import *
from base_obj import new_object
from physical_obj import PhysObj
from output_catcher import OutputCatcher
from player import Player
from packages.components.chair import ComponentChair


class TestClass():
    fresh_room: Room = None
    called_genesis: bool = False

    def generate_fresh_room(self):
        """
        Generate a new, fresh room for testing
        """
        if not self.called_genesis:
            self.called_genesis = True
            unit_test_genesis(False)

        global_textadv.qdel(self.fresh_room)

        self.fresh_room = Room("unit_test", "")

    def test_chair_component(self):
        self.generate_fresh_room()
        output_catcher: OutputCatcher = new_object(OutputCatcher)
        global_textadv.player_ref = new_object(Player)
        self.fresh_room.add_to_room(global_textadv.player_ref)
        chair: PhysObj = new_object(PhysObj, "reception_chair")
        chair_component: ComponentChair = chair.get_component(ComponentChair)
        self.fresh_room.add_to_room(chair)
        assert output_catcher.catch_output(
            global_textadv.player_ref.parse_text, ["sit in chair"], chair_component.sit_down_message)
        assert output_catcher.catch_output(
            global_textadv.player_ref.parse_text, ["get up from chair"], chair_component.get_up_message)
