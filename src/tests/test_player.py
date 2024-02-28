from room import Room
import global_textadv
from main import unit_test_genesis
from packages.verbs import *
from object import Object
from packages.verbs._verb import Verb
from global_textadv import get_subclasses_recursive
from re import search
from player import Player
from packages.components.inventory import ComponentInventory


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

    def test_text_parser(self):
        self.generate_fresh_room()
        global_textadv.player_ref = Player()
        assert (global_textadv.player_ref.get_component(ComponentInventory))

        self.fresh_room.add_to_room(global_textadv.player_ref)

        apple: Object = Object("apple")
        self.fresh_room.add_to_room(apple)

        global_textadv.player_ref.parse_text("pick up apple")

        assert (apple.location == global_textadv.player_ref.get_component(
            ComponentInventory))
        assert (apple.location != apple.current_room)
