from base_obj import BaseObj
from events.events import EVENT_UNIT_TEST_SIGNAL, EVENT_RETVAL_UNIT_TEST_SIGNAL_RESPOND


class SignalTestBaseObj(BaseObj):
    def __init__(self, object_id="") -> None:
        super().__init__(object_id)

        self.signal_recieved: bool = False

    def recieve_signal(self, source):
        """
        ### EVENT FUNCT
        """

        self.signal_recieved = True
        return EVENT_RETVAL_UNIT_TEST_SIGNAL_RESPOND


class TestClass():
    def test_signal_basic(self):
        obj_1: SignalTestBaseObj = SignalTestBaseObj()
        obj_2: SignalTestBaseObj = SignalTestBaseObj()

        obj_1.register_event(obj_1, EVENT_UNIT_TEST_SIGNAL,
                             obj_1.recieve_signal)

        obj_2.send_event(obj_1, EVENT_UNIT_TEST_SIGNAL)

        assert obj_1.signal_recieved

    def test_signal_crossobj(self):
        obj_1: SignalTestBaseObj = SignalTestBaseObj()
        obj_2: SignalTestBaseObj = SignalTestBaseObj()

        obj_2.register_event(obj_1, EVENT_UNIT_TEST_SIGNAL,
                             obj_2.recieve_signal)

        obj_1.send_event(obj_1, EVENT_UNIT_TEST_SIGNAL)

        assert obj_2.signal_recieved

    def test_signal_retval(self):
        obj_1: SignalTestBaseObj = SignalTestBaseObj()
        obj_2: SignalTestBaseObj = SignalTestBaseObj()

        obj_1.register_event(obj_1, EVENT_UNIT_TEST_SIGNAL,
                             obj_1.recieve_signal)

        return_value: int = obj_2.send_event(obj_1, EVENT_UNIT_TEST_SIGNAL)

        assert obj_1.signal_recieved
        assert return_value & EVENT_RETVAL_UNIT_TEST_SIGNAL_RESPOND
        assert return_value == EVENT_RETVAL_UNIT_TEST_SIGNAL_RESPOND
