from base_obj import BaseObj
from events.verb_events import EVENT_VERB_GET_UP
from ._verb import Verb
from ._verb_names import VERB_GET_UP
from bitflags import VERB_IGNORE_LAYDOWN, VERB_IGNORE_SITDOWN

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
        self.verb_flags = VERB_IGNORE_LAYDOWN | VERB_IGNORE_SITDOWN

    def execute_verb(self, owning_obj: BaseObj, arguments: list = []):
        self.send_event(owning_obj, EVENT_VERB_GET_UP)
