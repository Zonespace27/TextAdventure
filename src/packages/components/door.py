from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.verb_events import EVENT_VERB_OPEN_DOOR
from events.events import EVENT_DOOR_ATTEMPT_OPEN, EVENT_RETVAL_BLOCK_DOOR_OPEN
from ..verbs._verb_names import VERB_OPEN_DOOR
import global_textadv
from global_textadv import output
from traits import TRAIT_LOCKED
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from room import Room


class ComponentDoor(Component):
    id = "component_door"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # What room this door takes you to
        self.door_to: str = self.arg_set(args_dict, "door_to", str)

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        object_to_attach.add_verb(VERB_OPEN_DOOR)
        self.register_event(
            object_to_attach, EVENT_VERB_OPEN_DOOR, self.open_door)

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            phys_parent.remove_verb(VERB_OPEN_DOOR)
            self.unregister_event(phys_parent)

        return super().detach_from_parent()

    def open_door(self, source):
        """
        ### EVENT FUNCT
        """
        if self.parent.has_trait(TRAIT_LOCKED):
            output("You can't open this, it's locked!")
            return

        if self.send_event(self.parent, EVENT_DOOR_ATTEMPT_OPEN) & EVENT_RETVAL_BLOCK_DOOR_OPEN:
            return

        room_to_go_to: "Room" = global_textadv.roomid_to_room[self.door_to]
        global_textadv.player_ref.move_rooms(room_to_go_to)
