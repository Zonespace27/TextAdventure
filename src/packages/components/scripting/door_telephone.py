from .._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.events import EVENT_DOOR_ATTEMPT_OPEN, EVENT_RETVAL_BLOCK_DOOR_OPEN, EVENT_ENABLE_DIALOGUE, EVENT_DIALOGUE_COMPLETED
from global_textadv import qdel, output
from ...verbs._verb_names import VERB_OPEN_DOOR


class ComponentDoorTelephone(Component):
    id = "component_door_telephone"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # If the door has been opened before
        self.opened: bool = False

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(
            object_to_attach, EVENT_DOOR_ATTEMPT_OPEN, self.on_door_open)

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_DOOR_ATTEMPT_OPEN)
            telephone: PhysObj = phys_parent.current_room.get_content_object(
                "front_office_telephone")
            if telephone:
                self.unregister_event(telephone, EVENT_DIALOGUE_COMPLETED)

        return super().detach_from_parent()

    def on_door_open(self, source):
        """
        ### EVENT FUNCT
        """
        if not self.opened:
            output("As your hand moves to unlock the door, you hear the rotary phone on the reception desk behind you start to ring. You feel like you should probably answer.")
            self.opened = True
            phys_parent: PhysObj = self.parent
            self.send_event(phys_parent.current_room.get_content_object(
                "front_office_telephone"), EVENT_ENABLE_DIALOGUE)
            self.register_event(phys_parent.current_room.get_content_object(
                "front_office_telephone"), EVENT_DIALOGUE_COMPLETED, self.on_phonecall_finished)

        else:
            output(
                "You consider trying to leave the phone unanswered, but decide against it.")
        return EVENT_RETVAL_BLOCK_DOOR_OPEN

    def on_phonecall_finished(self, source):
        """
        ### EVENT FUNCT
        """

        qdel(self)
