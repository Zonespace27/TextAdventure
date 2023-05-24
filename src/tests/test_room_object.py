from room import Room
import globals
from main import unit_test_genesis
from player import Player
from object import Object
from packages.components.item import ComponentItem
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
        
        globals.qdel(self.fresh_room)

        self.fresh_room = Room("unit_test", "")

    
    def test_add_remove_room(self):
        self.generate_fresh_room()
        player_ref: Player = Player()

        self.fresh_room.add_to_room(player_ref)

        assert (player_ref in self.fresh_room.contents) # The player should be in the room now
        assert (player_ref.current_room == self.fresh_room) # And the player should know what room it's in

        object1 = Object("liquor_bottle")

        self.fresh_room.add_to_room(object1)

        assert (object1 in self.fresh_room.contents) # The object should be in the room
        assert (object1.current_room == self.fresh_room) # And it should know as well

        self.fresh_room.remove_from_room(player_ref)

        assert not (player_ref in self.fresh_room.contents) # They shouldn't be in the room now
        assert not (player_ref.current_room == self.fresh_room) # And they should know that, too

        globals.qdel(object1)

        assert (len(self.fresh_room.contents) == 0) # There shouldn't be anything in the room now
    

    def test_object_pickup(self):
        self.generate_fresh_room()
        globals.player_ref: Player = Player()

        self.fresh_room.add_to_room(globals.player_ref)

        object1 = Object("liquor_bottle")
        self.fresh_room.add_to_room(object1)

        inventory_component: ComponentInventory = globals.player_ref.get_component(ComponentInventory)

        item_component1: ComponentItem = object1.get_component(ComponentItem)
        item_component1.attempt_pickup(None)

        assert (object1 in inventory_component.inventory) # It should be in the inventory
        assert not (object1 in self.fresh_room.contents) # While not being in the room's contents
        assert (object1.current_room == self.fresh_room) # While still knowing what room it's in

        globals.qdel(globals.player_ref)