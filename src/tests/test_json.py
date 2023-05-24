from json import load
from packages.verbs import *
from packages.verbs._verb import Verb
from packages.components import *
from packages.components._component import Component
from packages.elements import *
from packages.elements._element import Element
from globals import get_subclasses_recursive

class TestClass():
    object_file_locs: list[str] = [ # Once i've got a concrete file structure down, i'll convert this to something better
        'json/objects.json',
        'json/doors.json',
    ]
    room_file_locs: list[str] = [ # Same here
        'json/rooms.json',
    ]

    def test_unique_object_ids(self):
        found_ids: list[str] = []
        for file in self.object_file_locs:
            data = load(open(file))
            for object_id in data:
                assert not (object_id in found_ids)
                found_ids.append(object_id)


    def test_valid_room_objects(self):
        found_object_ids: list[str] = []
        for file in self.object_file_locs:
            data = load(open(file))
            for object_id in data:
                found_object_ids.append(object_id)
        
        for file in self.room_file_locs:
            data = load(open(file))
            for room_id in data:
                if not ("objects" in data[room_id]):
                    continue
                
                for object in data[room_id]["objects"]:
                    assert (object in found_object_ids)
    

    def test_all_verbs_valid(self):
        found_verb_ids: list[str] = []
        verb_subclasses: list[Verb] = get_subclasses_recursive(Verb)
        for subclass in verb_subclasses:
            found_verb_ids.append(subclass.verb_id)
        
        for file in self.room_file_locs:
            data = load(open(file))
            for room_id in data:
                if not ("verbs" in data[room_id]):
                    continue
                
                for verb_id in data[room_id]["verbs"]:
                    assert (verb_id in found_verb_ids)
        
        for file in self.object_file_locs:
            data = load(open(file))
            for object_id in data:
                if not ("verbs" in data[object_id]):
                    continue            
    
                for verb_id in data[object_id]["verbs"]:
                    assert (verb_id in found_verb_ids)

    
    def test_all_components_valid(self):
        found_component_ids: list[str] = []
        component_subclasses: list[Component] = get_subclasses_recursive(Component)
        for subclass in component_subclasses:
            found_component_ids.append(subclass.id)
        
        for file in self.room_file_locs:
            data = load(open(file))
            for room_id in data:
                if not ("components" in data[room_id]):
                    continue
                
                for component_id in list(data[room_id]["components"].keys()):
                    assert (component_id in found_component_ids)
        
        for file in self.object_file_locs:
            data = load(open(file))
            for object_id in data:
                if not ("components" in data[object_id]):
                    continue            
                
                for component_id in list(data[object_id]["components"].keys()):
                    assert (component_id in found_component_ids)


    def test_all_elements_valid(self):
        found_element_ids: list[str] = []
        element_subclasses: list[Element] = get_subclasses_recursive(Element)
        for subclass in element_subclasses:
            found_element_ids.append(subclass.id)
        
        for file in self.room_file_locs:
            data = load(open(file))
            for room_id in data:
                if not ("elements" in data[room_id]):
                    continue
                
                for element_id in data[room_id]["elements"]:
                    assert (element_id in found_element_ids)
        
        for file in self.object_file_locs:
            data = load(open(file))
            for object_id in data:
                if not ("elements" in data[object_id]):
                    continue        
                
                for element_id in data[object_id]["elements"]:
                    assert (element_id in found_element_ids)