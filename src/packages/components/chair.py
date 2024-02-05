from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.verb_events import EVENT_VERB_SIT
from ..verbs._verb_names import VERB_SIT
from .sitting_down import ComponentSittingDown
import global_textadv


class ComponentChair(Component):
    id = "component_chair"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # The message to send to the user when sitting down
        self.sit_down_message: str = self.arg_set(
            args_dict, "sit_down_message", str) or "You sit down in the chair."
        # The message to send to the user when getting up
        self.get_up_message: str = self.arg_set(
            args_dict, "get_up_message", str) or "You get up from the chair."

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(object_to_attach, EVENT_VERB_SIT, self.on_sit)
        object_to_attach.add_verb(VERB_SIT)

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_VERB_SIT)
            phys_parent.remove_verb(VERB_SIT)

        return super().detach_from_parent()

    def on_sit(self, source):
        """
        ### EVENT FUNCT
        """
        print(self.sit_down_message)
        global_textadv.player_ref.add_component(
            ComponentSittingDown, {"get_up_message": self.get_up_message})
