from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.events import EVENT_INVENTORY_ADD_OBJECT, EVENT_RETVAL_BLOCK_INVENTORY_ADD, EVENT_INVENTORY_REMOVE_OBJECT, EVENT_RETVAL_BLOCK_INVENTORY_REMOVE, EVENT_BASEOBJ_PRINT_DESCRIPTION, EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION, EVENT_PHYSOBJ_LOCATION_MOVE, EVENT_ITEM_PICKED_UP, EVENT_ITEM_DROPPED
from events.verb_events import EVENT_VERB_PICKUP, EVENT_VERB_DROP
from ..verbs._verb_names import VERB_PICKUP, VERB_DROP
import global_textadv
from global_textadv import output


class ComponentItem(Component):
    id = "component_item"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # What the general examine of this item should be BEFORE it's picked up, moved, or otherwise altered.
        self.unmoved_examine: str = self.arg_set(
            args_dict, "unmoved_examine", str)

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(
            object_to_attach, EVENT_VERB_PICKUP, self.attempt_pickup)
        self.register_event(
            object_to_attach, EVENT_VERB_DROP, self.attempt_drop)
        self.register_event(
            object_to_attach, EVENT_BASEOBJ_PRINT_DESCRIPTION, self.on_examine)
        self.register_event(
            object_to_attach, EVENT_PHYSOBJ_LOCATION_MOVE, self.on_move)
        object_to_attach.add_verb(VERB_PICKUP)
        object_to_attach.add_verb(VERB_DROP)

    def detach_from_parent(self):
        obj_parent: PhysObj = self.parent

        if obj_parent:
            self.unregister_event(obj_parent, EVENT_VERB_PICKUP)
            self.unregister_event(obj_parent, EVENT_VERB_DROP)
            self.unregister_event(obj_parent, EVENT_BASEOBJ_PRINT_DESCRIPTION)
            self.unregister_event(obj_parent, EVENT_PHYSOBJ_LOCATION_MOVE)
            obj_parent.remove_verb(VERB_PICKUP)
            obj_parent.remove_verb(VERB_DROP)

        return super().detach_from_parent()

    # idk if anyone but players will be able to pick stuff up
    def attempt_pickup(self, source) -> bool:
        """
        ### EVENT FUNCT
        """

        if self.send_event(global_textadv.player_ref, EVENT_INVENTORY_ADD_OBJECT, self.parent) & EVENT_RETVAL_BLOCK_INVENTORY_ADD:
            return False

        self.send_event(self.parent, EVENT_ITEM_PICKED_UP)

        return True

    def attempt_drop(self, source) -> bool:
        """
        ### EVENT FUNCT
        """

        if self.send_event(global_textadv.player_ref, EVENT_INVENTORY_REMOVE_OBJECT, self.parent) & EVENT_RETVAL_BLOCK_INVENTORY_REMOVE:
            return False

        self.send_event(self.parent, EVENT_ITEM_DROPPED)

        return True

    def on_move(self, source):
        """
        ### EVENT FUNCT
        """

        self.unmoved_examine = ""

    def on_examine(self, source):
        """
        ### EVENT FUNCT
        """

        if not self.unmoved_examine:
            return

        output(self.unmoved_examine)

        return EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION
