from base_obj import BaseObj
import global_textadv
from events.unit_test_events import EVENT_UNIT_TEST_OUTPUT


class OutputCatcher(BaseObj):
    """
    An object that should only appear in unit testing, used for catching text outputted by the output() function
    """

    def __init__(self, object_id: str = "") -> None:
        super().__init__(object_id)
        global_textadv.output_catcher = self

        self.outputted_text: str = ""

    def catch_output(self, callback, args: list, expected_text: str) -> bool:
        self.register_event(self, EVENT_UNIT_TEST_OUTPUT, self.on_output)
        callback(*args)
        self.unregister_event(self, EVENT_UNIT_TEST_OUTPUT)
        return expected_text == self.outputted_text

    def on_output(self, source, text: str):
        """
        ### EVENT FUNCT
        """

        self.outputted_text = text
