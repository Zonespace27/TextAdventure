from physical_obj import PhysObj
from base_obj import BaseObj
from events.events import EVENT_LOCK_ATTEMPT_UNLOCK
from ._verb import Verb 
from ._verb_names import VERB_UNLOCK
from ..components.key import ComponentKey
from ..components.locked import ComponentLocked
from ..components.item import ComponentItem
from ..components.inventory import ComponentInventory
import globals

class VerbUnlock(Verb):
    """
    This verb is attached with the Key component, NOT the Locked component
    """
    verb_id = VERB_UNLOCK

    def __init__(self) -> None:
        super().__init__()
        self.expected_args = [ 
            PhysObj,
            PhysObj,
        ]
        self.action_strings = [
            "use",
            "unlock",
        ]
    

    def argument_is_valid(self, argument, index):
        if not isinstance(argument, PhysObj):
            return False

        argument: PhysObj
        if not (argument.location.__class__ == ComponentInventory):
            return False
        
        return super().argument_is_valid(argument, index)
    

    def can_attach_to(self, object_to_attach: BaseObj):
        if not object_to_attach.get_component(ComponentItem):
            return False
    
        if not isinstance(object_to_attach, PhysObj):
            return False

        return super().can_attach_to(object_to_attach)
    

    def try_execute_verb(self, owning_obj: PhysObj, arguments: list = []) -> bool:
        if len(arguments) < len(self.expected_args):
            return False
        
        if not (owning_obj == arguments[0]):
            return False
        
        if not (owning_obj.location == globals.player_ref.get_component(ComponentInventory)):
            return False
        
        object_to_unlock: PhysObj = arguments[1]
        if not object_to_unlock.get_component(ComponentLocked):
            return False

        return super().try_execute_verb(owning_obj, arguments)
        

    def execute_verb(self, owning_obj: BaseObj, arguments: list = []):
        key_component: ComponentKey = owning_obj.get_component(ComponentKey)
        self.send_event(arguments[1], EVENT_LOCK_ATTEMPT_UNLOCK, key_component.key_id)