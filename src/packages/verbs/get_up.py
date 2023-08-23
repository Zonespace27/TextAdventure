from base_obj import BaseObj
from events import EVENT_VERB_GET_UP
from ._verb import Verb
from ._verb_names import VERB_GET_UP
from ..components.laying_down import ComponentLayingDown
from bitflags import VERB_OVERRIDE_LAYDOWN

class VerbGetUp(Verb):
    verb_id = VERB_GET_UP

    def __init__(self) -> None:
        super().__init__()
        self.expected_args = []
        self.action_strings = [
            "stand",
            "stand up",
            "get up",
        ]
        self.verb_flags = VERB_OVERRIDE_LAYDOWN

    def try_execute_verb(self, owning_obj: BaseObj, arguments: list = []) -> bool:
        if not owning_obj.get_component(ComponentLayingDown):
            return False

        return super().try_execute_verb(owning_obj, arguments)


    def execute_verb(self, owning_obj: BaseObj, arguments: list = []):
        self.send_event(owning_obj, EVENT_VERB_GET_UP)
