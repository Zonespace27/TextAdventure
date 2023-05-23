from json import load
from packages.verbs import *
from packages.verbs._verb import Verb
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
                for verb_id in data[room_id]["verbs"]:
                    assert (verb_id in found_verb_ids)
        
        for file in self.object_file_locs:
            data = load(open(file))
            for object_id in data:
                for verb_id in data[object_id]["verbs"]:
                    assert (verb_id in found_verb_ids) # Ideally, I'd like to deprecate adding raw verbs by json (and make them be added via component instead), but until then, i'll test for it  

        