import object
import physical_obj
import events

class Room():

    def __init__(self, room_id: str, room_desc: str, room_objects: list[str], room_verbs: list[str]) -> None:
        self.id = room_id
        self.desc = room_desc

        self.contents: list[physical_obj.PhysObj] = []
        self.verbs = {}
        for obj in room_objects:
            self.objects.append(object.Object(obj))
        #TODO: Add verb implementation
    
    def add_to_room(self, physobj_to_add: physical_obj.PhysObj):
        self.contents.append(physobj_to_add)
        physobj_to_add.current_room = self

        for obj in self.contents:
            physobj_to_add.send_event(obj, events.EVENT_ROOM_PHYSOBJ_ENTERED, self)
    
    def remove_from_room(self, physobj_to_remove: physical_obj.PhysObj):
        self.contents.remove(physobj_to_remove)
        physobj_to_remove.current_room = None