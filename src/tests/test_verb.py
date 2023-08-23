from packages.verbs import *
from packages.verbs._verb import Verb
from globals import get_subclasses_recursive
from re import search

class TestClass():
    def test_verb_names(self):
        verb_ids: list[str] = [] # Verb IDs found from subclasses of Verb
        found_verb_names: list[str] = [] # Verb names found in the _verb_names.py file
        file = open('src/packages/verbs/_verb_names.py', "r")
        for line in file.readlines():
            result = search(r"VERB_[A-Z_]+ = \"([a-z_]+)\"", line)
            if not result.group(1):
                continue

            assert not (result.group(1) in found_verb_names) # We check to make sure there's no dupes
            found_verb_names.append(result.group(1))
        file.close()

        for subclass in get_subclasses_recursive(Verb):
            subclass: Verb
            assert not (subclass.verb_id in verb_ids) # And another check to ensure no dupes
            assert subclass.verb_id in found_verb_names # And finally making sure that every verb ID is in found_verb_names
            verb_ids.append(subclass.verb_id)
