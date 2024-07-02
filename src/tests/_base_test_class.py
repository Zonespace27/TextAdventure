from room import Room
from main import unit_test_genesis
import global_textadv
from output_catcher import OutputCatcher
from base_obj import new_object


class TestClass():
    fresh_room: Room = None
    called_genesis: bool = False
    output_catcher: OutputCatcher = None

    def init_things(self):
        """
        Must be called as the first line of any test. Tests can't use __init__ so this is what we have to work with instead.
        """

        if not self.called_genesis:
            self.called_genesis = True
            unit_test_genesis(False)

        if not self.output_catcher:
            self.output_catcher = new_object(OutputCatcher)

    def generate_fresh_room(self):
        """
        Generate a new, fresh room for testing
        """

        global_textadv.qdel(self.fresh_room)

        self.fresh_room = Room("unit_test", "")
