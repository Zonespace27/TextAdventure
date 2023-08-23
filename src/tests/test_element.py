from packages.elements import *
from packages.elements._element import Element
from globals import get_subclasses_recursive
from re import search

class TestClass():
    def test_element_names(self):
        element_ids: list[str] = [] # Element IDs found from subclasses of Element
        found_element_names: list[str] = [] # Element names found in the _element_names.py file
        file = open('src/packages/elements/_element_names.py', "r")
        for line in file.readlines():
            result = search(r"ELEMENT_[A-Z_]+ = \"([a-z_]+)\"", line)
            if not result.group(1):
                continue

            assert not (result.group(1) in found_element_names) # We check to make sure there's no dupes
            found_element_names.append(result.group(1))
        file.close()

        for subclass in get_subclasses_recursive(Element):
            subclass: Element
            assert not (subclass.id in element_ids) # And another check to ensure no dupes
            assert subclass.id in found_element_names # And finally making sure that every element ID is in found_element_names
            element_ids.append(subclass.id)
