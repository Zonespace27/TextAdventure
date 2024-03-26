from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.verb_events import EVENT_VERB_ANSWER_PHONE, EVENT_VERB_SPEAK
from events.events import EVENT_ENABLE_DIALOGUE, EVENT_DISABLE_DIALOGUE, EVENT_DIALOGUE_COMPLETED
from ..verbs._verb_names import VERB_ANSWER_PHONE, VERB_SPEAK
import global_textadv
from ..dialogue._node import DialogueNode


class ComponentDialogue(Component):
    id = "component_dialogue"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # The node ID of the starting dialogue message
        self.dialogue_node: str = self.arg_set(args_dict, "dialogue_node", str)

        # If this component is a telephone instead of a person
        self.telephone: bool = self.arg_set(args_dict, "telephone", bool)

        # If the dialogue is currently enabled
        self.enabled: bool = self.arg_set(args_dict, "enabled", bool)

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(
            object_to_attach, EVENT_ENABLE_DIALOGUE, self.enable_dialogue)
        self.register_event(
            object_to_attach, EVENT_DISABLE_DIALOGUE, self.disable_dialogue)

        if self.telephone:
            self.register_event(
                object_to_attach, EVENT_VERB_ANSWER_PHONE, self.on_start_speak)
            object_to_attach.add_verb(VERB_ANSWER_PHONE)
        else:
            self.register_event(
                object_to_attach, EVENT_VERB_SPEAK, self.on_start_speak)
            object_to_attach.add_verb(VERB_SPEAK)

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_ENABLE_DIALOGUE)
            self.unregister_event(phys_parent, EVENT_DISABLE_DIALOGUE)

            if self.telephone:
                self.unregister_event(phys_parent, EVENT_VERB_ANSWER_PHONE)
                phys_parent.remove_verb(VERB_ANSWER_PHONE)
            else:
                self.unregister_event(phys_parent, EVENT_VERB_SPEAK)
                phys_parent.remove_verb(VERB_SPEAK)

        return super().detach_from_parent()

    def on_start_speak(self, source):
        """
        ### EVENT FUNCT
        """
        if not self.enabled:
            return

        node: DialogueNode = global_textadv.dialogue_id_to_node[self.dialogue_node]
        node.trigger_node()
        self.send_event(self.parent, EVENT_DIALOGUE_COMPLETED)

    def enable_dialogue(self, source):
        """
        ### EVENT FUNCT
        """
        self.enabled = True

    def disable_dialogue(self, source):
        """
        ### EVENT FUNCT
        """
        self.enabled = False
