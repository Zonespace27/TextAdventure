from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.verb_events import EVENT_VERB_EAT
from global_textadv import qdel, output
from ..verbs._verb_names import VERB_EAT


class ComponentEdible(Component):
    id = "component_edible"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # How many bites this edible object has total
        self.total_bites: int = self.arg_set(args_dict, "total_bites", int)
        # How many bites this edible object has left
        self.remaining_bites: int = self.total_bites
        # The message sent to the user when this is eaten
        self.eat_message: str = self.arg_set(args_dict, "eat_message", str)
        # The message sent to the user when they've eaten the final bite
        self.final_eat_message: str = self.arg_set(
            args_dict, "final_eat_message", str)

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(object_to_attach, EVENT_VERB_EAT, self.on_eat)
        object_to_attach.add_verb(VERB_EAT)

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_VERB_EAT)
            phys_parent.remove_verb(VERB_EAT)

        return super().detach_from_parent()

    def on_eat(self, source):
        """
        ### EVENT FUNCT
        """
        if self.remaining_bites > 1:
            output(self.eat_message)
        else:
            output(self.final_eat_message)

        self.remaining_bites -= 1
        if self.remaining_bites <= 0:
            qdel(self.parent)
