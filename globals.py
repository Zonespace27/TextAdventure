import room
import player

def initialize_globals():
    # Dict of "roomid" : Room reference
    global roomid_to_room

    roomid_to_room: dict[str, room.Room] = {}

    # Dict of "objectid" : (dict of "data" : data)
    global object_id_data

    object_id_data: dict[str, dict[str]] = {}

    # Ref to the player
    global player_ref

    player_ref: player.Player = None