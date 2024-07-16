from ._component import Component
from .inventory import ComponentInventory
from base_obj import BaseObj
from physical_obj import PhysObj
from events.events import EVENT_BASEOBJ_PRINT_DESCRIPTION, EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION, EVENT_PLAYER_FIND_CONTENTS, EVENT_OBJECT_ADDED_TO_INVENTORY
from events.verb_events import EVENT_VERB_OPEN_CONTAINER, EVENT_VERB_CLOSE_CONTAINER, EVENT_VERB_EXAMINE
from ..verbs._verb_names import VERB_OPEN_CONTAINER, VERB_EXAMINE, VERB_CLOSE_CONTAINER
from traits import TRAIT_LOCKED
from base_obj import new_object
from global_textadv import output
from bitflags import BASEOBJ_BASE_EXAMINE_OVERRIDDEN


class ComponentContainer(Component):
    id = "component_container"

    def __init__(self, args_dict=dict[str]) -> None:
        super().__init__()

        self.contents: list[PhysObj] = []

        # If the container is open or closed
        self.open = self.arg_set(args_dict, "open", bool)
        # If the container needs to bother with being open or closed at all
        self.requires_open = self.arg_set(args_dict, "requires_open", bool)
        # If the container should visibly be open or closed
        self.open_visibility = self.arg_set(args_dict, "open_visibility", bool)
        # If the container should ever show its contents on examine
        self.show_contents_examine = self.arg_set(
            args_dict, "show_contents_examine", bool)
        # Message shown to the user when they open the container
        self.open_message = self.arg_set(
            args_dict, "open_message", str) or "You open the container."
        # Message shown to the user when they close the container
        self.close_message = self.arg_set(
            args_dict, "close_message", str) or "You close the container."
        # Message shown to the user when they examine the container, if it doesn't have an open/closed state
        self.no_open_close_examine_message = self.arg_set(
            args_dict, "no_open_close_examine_message", str) or "You look closer at the container."
        # Message shown to the user when they examine the container when it is open
        self.open_examine_message = self.arg_set(
            args_dict, "open_examine_message", str) or "You look closer at the container. Inside, you see:\n"
        # Message shown to the user when they examine the container when it is closed
        self.closed_examine_message = self.arg_set(
            args_dict, "closed_examine_message", str) or "You look closer at the container."
        # Message shown to the user when they look around the room that contains this container
        self.view_message = self.arg_set(
            args_dict, "view_message", str) or "It is"

        self.set_initial_contents(self.arg_set(
            args_dict, "initial_contents", list))

    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False

        object_to_attach: PhysObj

        self.register_event(
            object_to_attach, EVENT_VERB_OPEN_CONTAINER, self.open_container)
        self.register_event(
            object_to_attach, EVENT_VERB_CLOSE_CONTAINER, self.close_container)
        self.register_event(
            object_to_attach, EVENT_BASEOBJ_PRINT_DESCRIPTION, self.on_view)
        self.register_event(
            object_to_attach, EVENT_PLAYER_FIND_CONTENTS, self.get_contents)
        self.register_event(
            object_to_attach, EVENT_VERB_EXAMINE, self.on_examine)
        object_to_attach.add_verb(VERB_OPEN_CONTAINER)
        object_to_attach.add_verb(VERB_CLOSE_CONTAINER)
        object_to_attach.add_verb(VERB_EXAMINE)
        object_to_attach.baseobj_bitflags |= BASEOBJ_BASE_EXAMINE_OVERRIDDEN

        return super().attach_to_parent(object_to_attach)

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_VERB_OPEN_CONTAINER)
            self.unregister_event(phys_parent, EVENT_VERB_CLOSE_CONTAINER)
            self.unregister_event(phys_parent, EVENT_BASEOBJ_PRINT_DESCRIPTION)
            self.unregister_event(phys_parent, EVENT_PLAYER_FIND_CONTENTS)
            self.unregister_event(phys_parent, EVENT_VERB_EXAMINE)
            self.remove_verb(VERB_OPEN_CONTAINER)
            self.remove_verb(VERB_CLOSE_CONTAINER)
            self.remove_verb(VERB_EXAMINE)
            phys_parent.baseobj_bitflags &= ~BASEOBJ_BASE_EXAMINE_OVERRIDDEN

        return super().detach_from_parent()

    def set_initial_contents(self, content_list: list[str]):
        for entry in content_list:
            self.add_object(new_object(PhysObj, entry))

    def add_object(self, object: PhysObj, silent: bool = False):
        self.register_event(
            object, EVENT_OBJECT_ADDED_TO_INVENTORY, self.on_object_taken)
        self.contents.append(object)
        object.move_location(self.parent)

    def remove_object(self, object: PhysObj, silent: bool = False):
        self.unregister_event(object, EVENT_OBJECT_ADDED_TO_INVENTORY)
        self.contents.remove(object)

    def on_object_taken(self, source, inventory_owner: PhysObj, inventory: ComponentInventory):
        """
        ### EVENT FUNCT
        """
        self.remove_object(source)

    def open_container(self, source):
        """
        ### EVENT FUNCT
        """
        if self.open or (not self.requires_open):
            return

        if self.parent.has_trait(TRAIT_LOCKED):
            output("You can't open this, it's locked!")
            return

        self.open = True
        output(self.open_message)

    def close_container(self, source):
        """
        ### EVENT FUNCT
        """
        if (not self.open) or (not self.requires_open):
            return

        self.open = False
        output(self.close_message)

    def on_view(self, source) -> str:
        """
        ### EVENT FUNCT
        """
        if not self.requires_open:
            return

        phys_parent: PhysObj = self.parent
        open_or_close_string: str = f"{self.view_message} " + \
            ("open." if self.open else "closed.")

        output(f"{phys_parent.desc} {open_or_close_string}")
        return EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION

    def get_contents(self, source) -> list[PhysObj]:
        """
        ### EVENT FUNCT
        """
        if not self.requires_open:
            return self.contents

        return (self.contents if self.open else [])

    def get_content_item(self, object_id: str):
        for item in self.contents:
            if item.id != object_id:
                continue
            return item

    def on_examine(self, source):
        """
        ### EVENT FUNCT
        """
        if not self.requires_open:
            output(self.no_open_close_examine_message)
            if self.show_contents_examine:
                content_objects: str = ""
                for index, object in enumerate(self.contents):
                    content_objects += (object.name + (", " if index !=
                                        (len(self.contents) - 1) else "."))
                output(content_objects)
            return

        if self.open:
            output(self.open_examine_message)
            if self.show_contents_examine:
                content_objects: str = ""
                for index, object in enumerate(self.contents):
                    content_objects += (object.name + (", " if index !=
                                        (len(self.contents) - 1) else "."))
                output(content_objects)
        else:
            output(self.closed_examine_message)
