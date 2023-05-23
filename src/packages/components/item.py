from ._component import Component
from base_obj import BaseObj
from object import Object
from events import EVENT_VERB_PICKUP, EVENT_VERB_DROP, EVENT_INVENTORY_ADD_OBJECT, EVENT_RETVAL_BLOCK_INVENTORY_ADD, EVENT_INVENTORY_REMOVE_OBJECT, EVENT_RETVAL_BLOCK_INVENTORY_REMOVE
from ..verbs._verb_names import VERB_PICKUP, VERB_DROP
import globals

class ComponentItem(Component):
    id = "component_item"

    def __init__(self, args_dict = dict[str]) -> None:
        super().__init__()


    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, Object):
            return False
        
        object_to_attach: Object

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(object_to_attach, EVENT_VERB_PICKUP, self.attempt_pickup)
        self.register_event(object_to_attach, EVENT_VERB_DROP, self.attempt_drop)
        object_to_attach.add_verb(VERB_PICKUP)
        object_to_attach.add_verb(VERB_DROP)
    

    def detach_from_parent(self):
        obj_parent: Object = self.parent

        if obj_parent:
            self.unregister_event(obj_parent, EVENT_VERB_PICKUP)
            self.unregister_event(obj_parent, EVENT_VERB_DROP)
            obj_parent.remove_verb(VERB_PICKUP)
            obj_parent.remove_verb(VERB_DROP)

        return super().detach_from_parent()
    

    def attempt_pickup(self, source): #idk if anyone but players will be able to pick stuff up
        """
        ### EVENT FUNCT
        """

        if self.send_event(globals.player_ref, EVENT_INVENTORY_ADD_OBJECT, self.parent) == EVENT_RETVAL_BLOCK_INVENTORY_ADD:
            return False
        
        return True
        
    
    def attempt_drop(self, source):
        """
        ### EVENT FUNCT
        """

        if self.send_event(globals.player_ref, EVENT_INVENTORY_REMOVE_OBJECT, self.parent) == EVENT_RETVAL_BLOCK_INVENTORY_REMOVE:
            return False
        
        return True
