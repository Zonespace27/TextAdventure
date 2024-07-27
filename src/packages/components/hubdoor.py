from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from room import Room
from events.verb_events import EVENT_VERB_OPEN_DOOR
from events.events import EVENT_DOOR_ATTEMPT_OPEN, EVENT_RETVAL_BLOCK_DOOR_OPEN, EVENT_OBJECT_INITIALIZED
from ..verbs._verb_names import VERB_OPEN_DOOR
import global_textadv
from traits import TRAIT_LOCKED
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from room import Room


class ComponentHubDoor(Component):
    """
    Component used for doors that should send the user to a "hub" menu, where they can choose between different locations to go to.
    This allows for the user to quickly go between important POIs instead of meandering through streets that don't serve 
    """

    id = "component_hub_door"

    # Shared dict of {"hub_id" : {"room to go to" : Room}}, used to list what rooms can be gone to via this door/hub id
    hub_dict: dict[str, dict[str, Room]] = {}

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # What hub this door should open to
        self.hub_id: str = self.arg_set(args_dict, "hub_id", str) or "default"

        # Description of the room that this door is in
        self.room_desc: str = self.arg_set(args_dict, "room_desc", str)

        # Message to be sent to the player when traveling to this door's room
        self.travel_message: str = self.arg_set(
            args_dict, "travel_message", str)

        global_textadv.hubdoors.append(self)

    def dispose(self):
        global_textadv.hubdoors.remove(self)
        return super().dispose()

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        object_to_attach.add_verb(VERB_OPEN_DOOR)
        self.register_event(
            object_to_attach, EVENT_VERB_OPEN_DOOR, self.open_door)

        if not (self.hub_id in self.hub_dict):
            self.hub_dict[self.hub_id] = {}

        self.register_event(
            object_to_attach, EVENT_OBJECT_INITIALIZED, self.on_parent_init)

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            phys_parent.remove_verb(VERB_OPEN_DOOR)
            self.unregister_event(phys_parent)

        self.hub_dict[self.hub_id].pop(self.room_desc)

        return super().detach_from_parent()

    def open_door(self, source):
        """
        ### EVENT FUNCT
        """
        if self.parent.has_trait(TRAIT_LOCKED):
            print("You can't open this, it's locked!")
            return

        if self.send_event(self.parent, EVENT_DOOR_ATTEMPT_OPEN) & EVENT_RETVAL_BLOCK_DOOR_OPEN:
            return

        self.offer_transit_options()

    def offer_transit_options(self):
        phys_parent: PhysObj = self.parent
        offer_string: str = "Where would you like to go? (by number)\n"
        i: int = 0
        options: dict[str, Room] = self.hub_dict[self.hub_id].copy()
        options.pop(list(options.keys())[
                    list(options.values()).index(phys_parent.current_room)])
        options["Leave"] = None
        for option in options:
            offer_string += f"({i}) {option}\n"
            i += 1
        result: str = input(offer_string)

        if not result.isnumeric():  # this cancels opening the door, unlike most input methods. May want to correct someday, zonenote
            return

        chosen_string: str = list(options.keys())[int(result)]
        if chosen_string == "Leave":
            return

        if (self.travel_message):
            print(self.travel_message)

        global_textadv.player_ref.move_rooms(options[chosen_string])

    def on_parent_init(self, source):
        """
        EVENT FUNCT
        """

        phys_parent: PhysObj = self.parent
        if phys_parent.current_room:
            self.hub_dict[self.hub_id][self.room_desc] = phys_parent.current_room
        self.unregister_event(phys_parent, EVENT_OBJECT_INITIALIZED)
