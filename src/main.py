from packages.components import *
from packages.components._component import Component
from packages.verbs import *
import packages.verbs._verb as verbs
from json import load
import room
import globals
import player

def genesis():
    globals.initialize_globals() # Must be first
    assemble_verbs() # Must be before object init
    assemble_components() # Must be done before object init
    assemble_all_objects() # Must be before room init
    assemble_room_ids() # Must be after object init
    init_player() # Must be last


# Assembles objects, physobjects, items, etc.
def assemble_all_objects():
    file_locs: list[str] = [
        'json/objects.json',
        #'json/phys_objects.json',
    ]
    for file in file_locs:
        data = load(open(file))
        for object_id in data:

            # Ensures there's no runtimes in this code by giving objects default values
            if "name" not in data[object_id]:
                data[object_id]["name"] = ""
            if "alternate_names" not in data[object_id]:
                data[object_id]["alternate_names"] = []             
            if "desc" not in data[object_id]:
                data[object_id]["desc"] = ""
            if "verbs" not in data[object_id]:
                data[object_id]["verbs"] = []
            if "components" not in data[object_id]:
                data[object_id]["components"] = {}
            if "player_visible" not in data[object_id]:
                data[object_id]["player_visible"] = True

            verb_list: list[verbs.Verb] = []
            
            for verb_id in data[object_id]["verbs"]:
                verb_list.append(globals.verb_id_data[verb_id]) # Makes a list of verb singletons from a list of verb IDs

            globals.object_id_data[object_id] = {
                "name": data[object_id]["name"],
                "alternate_names": data[object_id]["alternate_names"],
                "desc": data[object_id]["desc"],
                "verbs": verb_list,
                "components": data[object_id]["components"],
                "player_visible": data[object_id]["player_visible"],
            }


def assemble_verbs():
    for subclass in globals.get_subclasses_recursive(verbs.Verb):
        new_subclass: verbs.Verb = subclass()
        globals.verb_id_data[new_subclass.verb_id] = new_subclass


def assemble_room_ids():
    data = load(open('json/rooms.json'))
    for room_id in data:
        globals.roomid_to_room[room_id] = room.Room(room_id, data[room_id]["desc"], data[room_id]["objects"], data[room_id]["verbs"])


def assemble_components():
    for subclass in globals.get_subclasses_recursive(Component):
        subclass: type[Component]
        globals.component_id_to_class[subclass.id] = subclass
    

def init_player():
    globals.player_ref = player.Player()
    globals.roomid_to_room["start"].add_to_room(globals.player_ref)
    globals.player_ref.begin_taking_input()


if __name__ == "__main__":
    genesis()
