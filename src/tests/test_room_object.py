from room import Room
import global_textadv
from base_obj import new_object
from main import unit_test_genesis
from player import Player
from physical_obj import PhysObj
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

        global_textadv.qdel(self.fresh_room)

        self.fresh_room = Room("unit_test", "")

    def test_add_remove_room(self):
        self.generate_fresh_room()
        player_ref: Player = Player()

        self.fresh_room.add_to_room(player_ref)

        # The player should be in the room now
        assert (player_ref in self.fresh_room.contents)
        # And the player should know what room it's in
        assert (player_ref.current_room == self.fresh_room)

        object1 = new_object(PhysObj, "liquor_bottle")

        self.fresh_room.add_to_room(object1)

        # The object should be in the room
        assert (object1 in self.fresh_room.contents)
        # And it should know as well
        assert (object1.current_room == self.fresh_room)

        self.fresh_room.remove_from_room(player_ref)

        # They shouldn't be in the room now
        assert not (player_ref in self.fresh_room.contents)
        # And they should know that, too
        assert not (player_ref.current_room == self.fresh_room)

        global_textadv.qdel(object1)

        # There shouldn't be anything in the room now
        assert (len(self.fresh_room.contents) == 0)

    def test_object_pickup(self):
        self.generate_fresh_room()
        global_textadv.player_ref = Player()

        self.fresh_room.add_to_room(global_textadv.player_ref)

        object1 = new_object(PhysObj, "liquor_bottle")
        self.fresh_room.add_to_room(object1)

        inventory_component: ComponentInventory = global_textadv.player_ref.get_component(
            ComponentInventory)

        item_component1: ComponentItem = object1.get_component(ComponentItem)
        item_component1.attempt_pickup(None)

        # It should be in the inventory
        assert (object1 in inventory_component.inventory)
        # While not being in the room's contents
        assert not (object1 in self.fresh_room.contents)
        # While still knowing what room it's in
        assert (object1.current_room == self.fresh_room)

        global_textadv.qdel(global_textadv.player_ref)
