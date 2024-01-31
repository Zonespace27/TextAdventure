from ._component import Component
from base_obj import BaseObj
from events.events import EVENT_BASEOBJ_PRINT_DESCRIPTION, EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION, EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION
import globals
from room import Room


class ComponentFirstEnterMessage(Component):
    id = "component_first_enter_message"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # What message is sent the first time the user enter the room
        self.enter_message: str = self.arg_set(args_dict, "enter_message", str)
        # If this should only block everything instead of just the room's description
        self.block_all_messages: bool = self.arg_set(
            args_dict, "block_all_messages", bool)

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, Room):
            return False

        object_to_attach: Room

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(
            object_to_attach, EVENT_BASEOBJ_PRINT_DESCRIPTION, self.send_message)

    def detach_from_parent(self):
        if self.parent:
            self.unregister_event(self.parent, EVENT_BASEOBJ_PRINT_DESCRIPTION)

        return super().detach_from_parent()

    def send_message(self, source):
        """
        ### EVENT FUNCT
        """
        print("\n" + self.enter_message)
        globals.qdel(self)
        return (EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION if self.block_all_messages else EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION)
