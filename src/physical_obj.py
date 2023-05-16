from typing import TYPE_CHECKING
import base_obj as base_obj
import globals

if TYPE_CHECKING:
    import room
    from packages.verbs._verb import Verb


class PhysObj(base_obj.BaseObj):
    """
    Anything physical inside a room (not the room itself) should be a child of this.
    Player, object, item, person, etc.
    """

    json_location: str = 'textadventure/json/phys_objects.json'
    
    def __init__(self, object_id: str) -> None:
        super().__init__(object_id)

        # The _primary_ name something will be referred to as
        self.name: str = ""
        # A list of all names that work for this, self.name is appended as well
        self.alternate_names: list[str] = []
        # A general, light description of this obj
        self.desc: str = ""
        
        # If this Obj should be visually in a room
        self.player_visible = True
        # The current room loc of this Obj
        self.current_room: "room.Room" = None

        if object_id:
            self.name = globals.object_id_data[object_id]["name"]
            self.alternate_names = globals.object_id_data[object_id]["alternate_names"]
            self.desc = globals.object_id_data[object_id]["desc"]
        
        self.alternate_names.append(self.name)
    

    def dispose(self):
        if self.current_room:
            self.current_room.remove_from_room(self, True)
        return super().dispose()

    
    def move_rooms(self, new_room: "room.Room"):
        self.current_room.remove_from_room(self)
        new_room.add_to_room(self)
    

    def action_is_valid(self, action_string: str) -> "Verb":
        for verb in self.source_verbs:
            if verb.action_string_is_valid(self, action_string):
                return verb
        return None
    

    def name_is_valid(self, name_to_try: str) -> bool:
        """
        A method used to check if a proposed name is valid for this physical object
        """
        if name_to_try.lower() in self.alternate_names:
            return True
        return False


    def add_verb(self, verb_id: str) -> bool:
        if verb_id not in globals.verb_id_data:
            return False
        
        if globals.verb_id_data[verb_id] in self.source_verbs:
            return True

        self.source_verbs.append(globals.verb_id_data[verb_id])
        return True

    def remove_verb(self, verb_id: str) -> bool:
        if verb_id not in globals.verb_id_data:
            return False
    
        if not (globals.verb_id_data[verb_id] in self.source_verbs):
            return True
        
        self.source_verbs.remove(globals.verb_id_data[verb_id])
        return True