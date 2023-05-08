from json import load
import room
import globals
import player

def genesis():
    globals.initialize_globals() # Must be first
    assemble_objects() # Must be before room init
    assemble_room_ids() # Must be after object init
    init_player() # Must be last

def assemble_objects():
    data = load(open('textadventure/json/objects.json')) # Once multiple files exist, i'll need a better system
    for object_id in data:
        globals.object_id_data[object_id] = {
            "name": data[object_id]["name"],
            "desc": data[object_id]["desc"],
        }

def assemble_room_ids():
    data = load(open('textadventure/json/rooms.json'))
    for room_id in data:
        globals.roomid_to_room[room_id] = room.Room(room_id, data[room_id]["desc"], data[room_id]["objects"], data[room_id]["verbs"])

def init_player():
    globals.player_ref = player.Player()
    globals.roomid_to_room["start"].add_to_room(globals.player_ref)


if __name__ == "__main__":
    genesis()
