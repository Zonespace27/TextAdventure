from ._component import Component
from physical_obj import PhysObj
from base_obj import BaseObj
import globals
from events.events import EVENT_LOCK_ATTEMPT_UNLOCK, EVENT_BASEOBJ_PRINT_DESCRIPTION
from traits import TRAIT_LOCKED


class ComponentLocked(Component):
    id = "component_locked"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        # What ComponentKey id is needed to unlock this lock
        self.lock_id: str = self.arg_set(args_dict, "lock_id", str) or "lock"
        # The message shown to the user on unlock
        self.unlock_message: str = self.arg_set(
            args_dict, "unlock_message", str) or "You unlock the thing."
        # A message to show when the parent is examined. Will not trigger if message is empty
        self.examine_message: str = self.arg_set(
            args_dict, "examine_message", str)

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        object_to_attach.add_trait(TRAIT_LOCKED, f"{self.id}_{self.lock_id}")
        self.register_event(
            object_to_attach, EVENT_LOCK_ATTEMPT_UNLOCK, self.unlock)
        self.register_event(
            object_to_attach, EVENT_BASEOBJ_PRINT_DESCRIPTION, self.on_view)

    def detach_from_parent(self):
        physobj_parent: PhysObj = self.parent

        if physobj_parent:
            physobj_parent.remove_trait(
                TRAIT_LOCKED, f"{self.id}_{self.lock_id}")

        return super().detach_from_parent()

    def unlock(self, source, key_id: str):
        """
        ### EVENT FUNCT
        """
        if not (key_id == self.lock_id):
            print("You try to insert the key into the lock, only for it to not fit.")
            return

        print(self.unlock_message)
        globals.qdel(self)

    def on_view(self, source):
        """
        ### EVENT FUNCT
        """
        if not (self.examine_message):
            return

        print(self.examine_message)
