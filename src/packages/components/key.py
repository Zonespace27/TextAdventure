from ._component import Component
from physical_obj import PhysObj
from base_obj import BaseObj
from ..verbs._verb_names import VERB_UNLOCK
from traits import TRAIT_LOCKED

class ComponentKey(Component):
    id = "component_key"

    def __init__(self, args_dict = dict[str]) -> None:
        super().__init__()

        # What ComponentLocked id this will unlock
        self.key_id: str = self.arg_set(args_dict, "key_id", str) or "lock" # Default value is the same as the default lock value


    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False
        
        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False
        
        object_to_attach.add_verb(VERB_UNLOCK)


    def detach_from_parent(self):
        physobj_parent: PhysObj = self.parent

        if physobj_parent:
            physobj_parent.remove_verb(VERB_UNLOCK)

        return super().detach_from_parent()
