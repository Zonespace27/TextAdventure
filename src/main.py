from packages.components import *
from packages.components.scripting import *
from packages.components._component import Component
from packages.components.laying_down import ComponentLayingDown
from packages.dialogue._node import DialogueNode
from packages.dialogue.phone.phone_node import PhoneNode
from packages.verbs import *
import packages.verbs._verb as verbs
from packages.elements import *
from packages.elements._element import Element
from json import load
import room
import global_textadv
from base_obj import new_object
import player
from os import system, getcwd, chdir
from time import sleep
import asyncio
from localization import Localization


def genesis():
    global_textadv.initialize_globals()  # Must be first
    assemble_verbs()  # Must be before object init
    assemble_components()  # Must be before object init
    assemble_elements()  # Must be before object init
    assemble_dialogue()  # Must be before object init
    assemble_all_objects()  # Must be before room init
    assemble_room_ids()  # Must be after object init
    assemble_hubdoors()  # Must be after room init
    Localization.generate_localization()  # Must be before player init
    init_player()  # Must be last


def unit_test_genesis(load_all_rooms: bool = False):
    """
    A version of genesis() used for unit testing so only necessary things are loaded
    """
    global_textadv.initialize_globals()  # Must be first
    assemble_verbs()  # Must be before object init
    assemble_components()  # Must be before object init
    assemble_elements()  # Must be before object init
    assemble_dialogue()  # Must be before object init
    assemble_all_objects()  # Must be before room init
    if load_all_rooms:
        assemble_room_ids()  # Must be after object init

# Assembles objects, physobjects, items, etc.


def assemble_all_objects():
    file_locs: list[str] = [
        global_textadv.resource_path('json/objects.json'),
        global_textadv.resource_path('json/doors.json'),
        global_textadv.resource_path('json/objects/containers.json'),
        global_textadv.resource_path('json/objects/items.json')
    ]
    for file in file_locs:
        opened_file = open(file)
        data = load(opened_file)
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
            if "elements" not in data[object_id]:
                data[object_id]["elements"] = []

            verb_list: list[verbs.Verb] = []

            for verb_id in data[object_id]["verbs"]:
                # Makes a list of verb singletons from a list of verb IDs
                verb_list.append(global_textadv.verb_id_data[verb_id])

            global_textadv.object_id_data[object_id] = {
                "name": data[object_id]["name"],
                "alternate_names": data[object_id]["alternate_names"],
                "desc": data[object_id]["desc"],
                "verbs": verb_list,
                "components": data[object_id]["components"],
                "elements": data[object_id]["elements"]
            }
        opened_file.close


def assemble_verbs():
    for subclass in global_textadv.get_subclasses_recursive(verbs.Verb):
        new_subclass: verbs.Verb = subclass()
        global_textadv.verb_id_data[new_subclass.verb_id] = new_subclass


def assemble_room_ids():
    file = open(global_textadv.resource_path('json/rooms.json'))
    data = load(file)
    for room_id in data:
        if not ("desc" in data[room_id]):
            data[room_id]["desc"] = ""
        if not ("objects" in data[room_id]):
            data[room_id]["objects"] = []
        if not ("verbs" in data[room_id]):
            data[room_id]["verbs"] = []
        if not ("components" in data[room_id]):
            data[room_id]["components"] = {}
        if not ("elements" in data[room_id]):
            data[room_id]["elements"] = []

        global_textadv.roomid_to_room[room_id] = new_object(room.Room, room_id, data[room_id]["desc"], data[room_id]
                                                            ["objects"], data[room_id]["verbs"], data[room_id]["components"], data[room_id]["elements"])
    file.close()


def assemble_dialogue():
    file_locs: list[str] = [
        global_textadv.resource_path('json/dialogue/phone.json'),
    ]
    for file in file_locs:
        opened_file = open(file)
        data = load(opened_file)
        for node_id in data:
            if not ("text" in data[node_id]):
                data[node_id]["text"] = ""
            if not ("select_text" in data[node_id]):
                data[node_id]["select_text"] = ""
            if not ("result_nodes" in data[node_id]):
                data[node_id]["result_nodes"] = []
            if not ("leave_allowed" in data[node_id]):
                data[node_id]["leave_allowed"] = False
            if not ("one_use_node" in data[node_id]):
                data[node_id]["one_use_node"] = False
            if not ("added_nodes" in data[node_id]):
                data[node_id]["added_nodes"] = []
            if not ("special_leave_text" in data[node_id]):
                data[node_id]["special_leave_text"] = ""

            new_node: DialogueNode
            # We want to allow for custom functionality in nodes
            if ("class_name" in data[node_id]):
                node_class = globals()[data[node_id]["class_name"]]
                new_node = node_class(node_id, data[node_id]["text"], data[node_id]["select_text"],
                                      data[node_id]["result_nodes"], data[node_id]["leave_allowed"], data[node_id]["one_use_node"], data[node_id]["added_nodes"], data[node_id]["special_leave_text"])

            else:
                new_node = DialogueNode(
                    node_id, data[node_id]["text"], data[node_id]["select_text"], data[node_id]["result_nodes"], data[node_id]["leave_allowed"], data[node_id]["one_use_node"],  data[node_id]["added_nodes"], data[node_id]["special_leave_text"])

            global_textadv.dialogue_id_to_node[node_id] = new_node
        opened_file.close()


def assemble_components():
    for subclass in global_textadv.get_subclasses_recursive(Component):
        subclass: type[Component]
        global_textadv.component_id_to_class[subclass.id] = subclass


def init_player():
    global_textadv.player_ref = new_object(player.Player)
    global_textadv.roomid_to_room["office_backroom"].add_to_room(
        global_textadv.player_ref)
    global_textadv.player_ref.add_component(ComponentLayingDown, {
        "get_up_message": "You get up from the floor, accidentally knocking away an empty bottle. You look down at your clothes, your form a general mess. Your dress shirt is stained with a few different substances, your coat looks like it's been in the possession of a dozen cats, and your shoes... is that vomit on them? Eugh. Though, it might be a good idea to look around instead of staring at your clothes."})
    asyncio.run(global_textadv.player_ref.begin_taking_input())


def assemble_elements():
    for subclass in global_textadv.get_subclasses_recursive(Element):
        new_subclass: Element = new_object(subclass)
        global_textadv.element_id_to_ref[new_subclass.id] = new_subclass


def assemble_hubdoors():
    for hubdoor in global_textadv.hubdoors:
        hubdoor.on_parent_init(None)


if __name__ == "__main__":
    if getcwd().endswith("\\src"):  # Gross hack that works for .bat junk
        chdir(getcwd().removesuffix("\\src"))

    # if global_textadv.unit_testing:
     #   pytest.main()

    else:
        """input("Welcome to [WHATEVER I'M CALLING THIS], press the ENTER key to start.") # A working 'welcome' screen that'll stick around for as I don't switch to wincurses (aka lose the will to live)
        system("cls")
        sleep(0.5)
        output("You are a down-on-their-luck detective, Mortimer Stevens. Mortimer is the PI (and sole employee) of the aptly named \"Mortimer & Co. Investigations\", located [PLACE].")
        sleep(0.5)
        output("Work hasn't been great recently, you've been getting steadily fewer clients as the weeks and months go by, but since it's just you, you're still in business.")
        sleep(0.5)
        output("However, a possible client called a few days ago, asking for a consultation. You scheduled it for April 19th.")
        sleep(1)
        input("Press ENTER to begin.")
        system("cls")"""  # Undo me when in prod
        genesis()
