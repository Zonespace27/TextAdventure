from typing import TYPE_CHECKING
import sys
from os import path, getcwd
import argparse

if TYPE_CHECKING:
    from base_obj import BaseObj

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

    parser = argparse.ArgumentParser(description='Run the program.')
    parser.add_argument('-d', '--development', action='store_true')

    args = parser.parse_args()

    # If we are running development mode or not, affecting some backend things
    global development_mode

    #development_mode = args.development
    development_mode = False # Fix me later when i figure out what the fuck the exe is looking for


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
    del object_to_delete


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    return relative_path # Yet another thing to fix later when EXE has been figured out
    #base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__ if not development_mode else getcwd())))
   # return path.join(base_path, relative_path)