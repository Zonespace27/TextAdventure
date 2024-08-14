from .._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.events import EVENT_DOOR_ATTEMPT_OPEN, EVENT_RETVAL_BLOCK_DOOR_OPEN, EVENT_ENABLE_DIALOGUE, EVENT_DIALOGUE_COMPLETED, EVENT_ITEM_PICKED_UP, EVENT_ITEM_DROPPED
from global_textadv import qdel, output
from ...verbs._verb_names import VERB_OPEN_DOOR
from room import Room
import global_textadv
from ..container import ComponentContainer


class ComponentDoorTelephone(Component):
    id = "component_door_telephone"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # If the door has been opened before
        self.opened: bool = False

        # If we've grabbed the forensics kit yet
        self.forensics_kit_taken: bool = False

        # Is TRUE once the phone is fully answered
        self.phone_answered: bool = False

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
        if self.phone_answered and not self.forensics_kit_taken:
            output(
                "You realize that you shouldn't leave your forensics kit behind when doing a forensical investigation.")
            return EVENT_RETVAL_BLOCK_DOOR_OPEN

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

        self.phone_answered = True
        office_backroom: Room = global_textadv.roomid_to_room["office_backroom"]
        safe_container: ComponentContainer = office_backroom.get_content_object(
            "wall_safe").get_component(ComponentContainer)
        forensic_kit: PhysObj = safe_container.get_content_item("forensic_kit")
        self.register_event(forensic_kit, EVENT_ITEM_PICKED_UP,
                            self.on_forensic_picked_up)
        self.register_event(forensic_kit, EVENT_ITEM_DROPPED,
                            self.on_forensic_dropped)

        # add some message here i dunno
        # "as you put down the phone, you feel like you should go get your forensics kit"
        # qdel(self)

    def on_forensic_picked_up(self, source):
        self.forensics_kit_taken = True

    def on_forensic_dropped(self, source):
        self.forensics_kit_taken = False
