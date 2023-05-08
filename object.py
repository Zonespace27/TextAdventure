from json import load
import globals
import physical_obj

class Object(physical_obj.PhysObj):
    json_location: str = 'textadventure/json/objects.json'
    
    def __init__(self, object_id: str) -> None:
        self.name: str = ""
        self.desc: str = ""

        if object_id:
            self.name = globals.object_id_data[object_id]["name"]
            self.desc = globals.object_id_data[object_id]["desc"]
        
