from base_obj import BaseObj
from events.verb_events import EVENT_VERB_SIT
from ._verb import Verb
from ._verb_names import VERB_SIT
from ..components.chair import ComponentChair
from physical_obj import PhysObj


class VerbSit(Verb):
    verb_id = VERB_SIT

    def __init__(self) -> None:
        super().__init__()
        self.expected_args = [
            PhysObj,
        ]
        self.action_strings = [
            "sit",
            "sit down",
            "rest",
        ]

    def can_execute_verb(self, owning_obj: BaseObj, arguments: list = []) -> bool:
        if len(arguments) < len(self.expected_args):
            return False

        if not self.check_object_argument(owning_obj, arguments, 0):
            return False

        if not owning_obj.get_component(ComponentChair):
            return False

        return super().can_execute_verb(owning_obj, arguments)

    def execute_verb(self, owning_obj: BaseObj, arguments: list = []):
        self.send_event(owning_obj, EVENT_VERB_SIT)
