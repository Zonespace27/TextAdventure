from physical_obj import PhysObj
import events.events as events
import base_obj as base_obj
import global_textadv


class Room(base_obj.BaseObj):

    def __init__(self, room_id: str, room_desc: str, room_objects: list[str] = [], room_verbs: list[str] = [], room_components: dict[str, dict[str]] = {}, room_elements: list[str] = []) -> None:
        super().__init__()

        self.id = room_id
        self.desc = room_desc

        self.contents: list[PhysObj] = []
        self.verbs = {}
        for obj in room_objects:
            self.add_to_room(PhysObj(obj))

        for verb in room_verbs:
            self.add_verb(verb)

        for component in list(room_components.keys()):
            self.add_component(
                global_textadv.component_id_to_class[component], room_components[component])

        for element in room_elements:
            self.add_element(element)

        global_textadv.roomid_to_room[room_id] = self

    def add_to_room(self, physobj_to_add: PhysObj):
        for obj in self.contents:
            physobj_to_add.send_event(
                obj, events.EVENT_ROOM_PHYSOBJ_ENTERED, self)

        self.contents.append(physobj_to_add)
        physobj_to_add.current_room = self
        # This one is explicitly not using the location_move function
        physobj_to_add.location = self

        self.send_event(
            physobj_to_add, events.EVENT_PHYSOBJ_ENTERED_ROOM, self)

    def remove_from_room(self, physobj_to_remove: PhysObj, deleted: bool = False):
        # This can happen when an object is in an inventory but then moves rooms
        if (physobj_to_remove in self.contents):
            self.contents.remove(physobj_to_remove)
        physobj_to_remove.current_room = None

    def remove_from_contents(self, physobj_to_remove: PhysObj):
        """
        A method that removes an object from a room's contents without nulling out its current room. \n
        Useful for things like an object being in an inventory.
        """
        self.contents.remove(physobj_to_remove)

    def get_content_object(self, object_id: str) -> PhysObj:
        """
        Get an object from this room's contents when given an object id
        """
        for object in self.contents:
            if object.id == object_id:
                return object
