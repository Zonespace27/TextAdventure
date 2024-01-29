from .._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.verb_events import EVENT_VERB_OPEN_DOOR
from events.events import EVENT_DOOR_ATTEMPT_OPEN, EVENT_RETVAL_BLOCK_DOOR_OPEN
from globals import qdel
from ...verbs._verb_names import VERB_OPEN_DOOR

class ComponentDoorTelephone(Component):
    id = "component_door_telephone"

    def __init__(self, args_dict = dict[str]) -> None:
        super().__init__()

        # If the door has been opened before
        self.opened: bool = False

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False
        
        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(object_to_attach, EVENT_DOOR_ATTEMPT_OPEN, self.on_door_open)
        object_to_attach.add_verb(VERB_OPEN_DOOR)
    

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_DOOR_ATTEMPT_OPEN)
            phys_parent.remove_verb(VERB_OPEN_DOOR)


        return super().detach_from_parent()
    

    def on_door_open(self, source):
        """
        ### EVENT FUNCT
        """
        if not self.opened:
            print("As your hand moves to unlock the door, you hear the rotary phone on the reception desk behind you start to ring. You feel like you should probably answer.")
            self.opened = True
        else:
            print("You consider trying to leave the phone unanswered, but decide against it.")
        return EVENT_RETVAL_BLOCK_DOOR_OPEN
