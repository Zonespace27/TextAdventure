from ._element import Element
from ._element_names import ELEMENT_INVISIBLE
from base_obj import BaseObj
from events.events import EVENT_BASEOBJ_PRINT_DESCRIPTION, EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION


class ElementInvisible(Element):
    """
    An element that is used to block something from appearing to the player whenever it would normally be seen.
    """
    id: str = ELEMENT_INVISIBLE

    def hook_object(self, object_to_hook: BaseObj) -> bool:
        self.register_event(
            object_to_hook, EVENT_BASEOBJ_PRINT_DESCRIPTION, self.block_examine)
        return super().hook_object(object_to_hook)

    def unhook_object(self, object_to_unhook: BaseObj) -> bool:
        self.unregister_event(
            object_to_unhook, EVENT_BASEOBJ_PRINT_DESCRIPTION)
        return super().unhook_object(object_to_unhook)

    def block_examine(self, source):
        """
        ### EVENT FUNCT
        """
        return EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION
