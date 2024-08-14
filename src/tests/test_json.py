from ._base_test_class import TestClass
from json import load
from packages.verbs import *
from packages.verbs._verb import Verb
from packages.components import *
from packages.components._component import Component
from packages.elements import *
from packages.elements._element import Element
from packages.dialogue import *
from packages.dialogue.phone import *
from packages.dialogue.phone.phone_node import PhoneNode
from global_textadv import get_subclasses_recursive, resource_path
import global_textadv
import pytest
from localization import Localization
import pytest

class TestClass2(TestClass):
    object_file_locs: list[str] = global_textadv.object_files
    room_file_locs: list[str] = global_textadv.room_files
    dialogue_file_locs: list[str] = global_textadv.dialogue_files
    localization_file_locs: list[str] = global_textadv.localization_files
    
    def test_unique_object_ids(self):
        self.init_things()
        found_ids: list[str] = []
        for file in self.object_file_locs:
            data = load(open(file))
            for object_id in data:
                assert not (object_id in found_ids)
                found_ids.append(object_id)

    def test_valid_room_objects(self):
        self.init_things()
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
        self.init_things()
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
        self.init_things()
        found_component_ids: list[str] = []
        component_subclasses: list[Component] = get_subclasses_recursive(
            Component)
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
        self.init_things()
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

    def test_all_dialogue_valid(self):
        self.init_things()
        found_dialogue_ids: list[str] = []
        for file in self.dialogue_file_locs:
            data = load(open(file))
            for dialogue_id in data:
                assert not (dialogue_id in found_dialogue_ids)

                found_dialogue_ids.append(dialogue_id)

                # Having text is necessary, but having select test is not, so we don't test for that
                assert ("text" in data[dialogue_id])
                assert (data[dialogue_id]["text"] != "")

                if ("class_name" in data[dialogue_id]):
                    try:
                        globals()[data[dialogue_id]["class_name"]]
                    except KeyError:
                        pytest.fail(
                            f"class_name of {dialogue_id} is not a valid class")

    def test_valid_localization_files(self):
        self.init_things()
        for file in self.localization_file_locs:
            # It throws an exception if the json is incorrectly formatted already, so we can just run through every language that way
            Localization.generate_localization(file)
            Localization.localization_dict = {}
