from typing import TYPE_CHECKING
from sys import getrefcount
from os import path, getcwd
# import argparse
from gc import get_referrers

if TYPE_CHECKING:
    from base_obj import BaseObj

# If True, will print any remaining references to an object on qdel
GC_HUNTING = False

# If True, will run the code in unit testing mode
UNIT_TESTING = False


def initialize_globals():
    # Dict of "roomid" : Room reference
    global roomid_to_room

    roomid_to_room = {}

    # Dict of "objectid" : (dict of "data" : data)
    global object_id_data

    object_id_data = {}

    # Dict of "phys_objid" : (dict of "data" : data)
    global phys_obj_id_data

    phys_obj_id_data = {}

    # Dict of "verb_id" : Verb object
    global verb_id_data

    verb_id_data = {}

    # Ref to the player
    global player_ref

    player_ref = None

    # Dict of "component_id" : Component class
    global component_id_to_class

    component_id_to_class = {}

    # Dict of "element_id" : Element singleton ref
    global element_id_to_ref

    element_id_to_ref = {}

    # Dict of "dialogue_id" : Dialogue node
    global dialogue_id_to_node

    dialogue_id_to_node = {}

    # parser = argparse.ArgumentParser(description='Run the program.')
    # parser.add_argument('-d', '--development', action='store_true')
    # parser.add_argument('--cov', action='codecov_enabled')

    # args = parser.parse_args()

    # If we are running development mode or not, affecting some backend things
    global development_mode

    # development_mode = args.development
    # Fix me later when i figure out what the fuck the exe is looking for
    development_mode = False


def get_subclasses_recursive(class_to_use: type) -> list[type]:
    return_list: list[type] = []
    for subclass in class_to_use.__subclasses__():
        return_list.append(subclass)
        return_list.extend(get_subclasses_recursive(subclass))

    return return_list


def qdel(object_to_delete: "BaseObj"):
    """
    Use this over the `del` function to delete objects
    """
    if object_to_delete:
        object_to_delete.dispose()

    if GC_HUNTING:
        referrers = get_referrers(object_to_delete)
        print(f"References of {object_to_delete}: {getrefcount(referrers)}")
        print(str(referrers))

    del object_to_delete


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    return relative_path  # Yet another thing to fix later when EXE has been figured out
    # base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__ if not development_mode else getcwd())))
   # return path.join(base_path, relative_path)
