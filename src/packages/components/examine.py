from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.verb_events import EVENT_VERB_EXAMINE
from ..verbs._verb_names import VERB_EXAMINE
from global_textadv import output


class ComponentExamine(Component):
    id = "component_examine"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # The text to show the player when examining the parent
        self.examine_text = self.arg_set(args_dict, "examine_text", str)

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(
            object_to_attach, EVENT_VERB_EXAMINE, self.on_examine)
        object_to_attach.add_verb(VERB_EXAMINE)

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_VERB_EXAMINE)
            phys_parent.remove_verb(VERB_EXAMINE)

        return super().detach_from_parent()

    def on_examine(self, source):
        """
        ### EVENT FUNCT
        """
        output(self.examine_text)
