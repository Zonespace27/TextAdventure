from physical_obj import PhysObj
from base_obj import BaseObj
from events.verb_events import EVENT_VERB_PICKUP
from ._verb import Verb
from ._verb_names import VERB_PICKUP
from ..components.item import ComponentItem
from ..components.inventory import ComponentInventory
import global_textadv


class VerbPickup(Verb):
    verb_id = VERB_PICKUP

    def __init__(self) -> None:
        super().__init__()
        self.expected_args = [
            PhysObj,
        ]
        self.action_strings = [
            "pickup",
            "take",
            "pick up",
            "grab",
            "nab",
        ]

    def argument_is_valid(self, argument, index):
        if not isinstance(argument, PhysObj):
            return False

        argument: PhysObj
        if argument.location.__class__ == ComponentInventory:
            return False

        return super().argument_is_valid(argument, index)

    def can_attach_to(self, object_to_attach: BaseObj):
        if not object_to_attach.get_component(ComponentItem):
            return False

        if not isinstance(object_to_attach, PhysObj):
            return False

        return super().can_attach_to(object_to_attach)

    def can_execute_verb(self, owning_obj: PhysObj, arguments: list = []) -> bool:
        if len(arguments) < len(self.expected_args):
            return False

        if not self.check_object_argument(owning_obj, arguments, 0):
            return False

        if (owning_obj.location == global_textadv.player_ref.get_component(ComponentInventory)):
            return False

        return super().can_execute_verb(owning_obj, arguments)

    def execute_verb(self, owning_obj: BaseObj, arguments: list = []):
        self.send_event(owning_obj, EVENT_VERB_PICKUP)
