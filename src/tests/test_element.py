from packages.elements import *
from packages.elements._element import Element
from globals import get_subclasses_recursive
from re import search


class TestClass():
    def test_element_names(self):
        # Element IDs found from subclasses of Element
        element_ids: list[str] = []
        # Element names found in the _element_names.py file
        found_element_names: list[str] = []
        file = open('src/packages/elements/_element_names.py', "r")
        for line in file.readlines():
            result = search(r"ELEMENT_[A-Z_]+ = \"([a-z_]+)\"", line)
            if not result.group(1):
                continue

            # We check to make sure there's no dupes
            assert not (result.group(1) in found_element_names)
            found_element_names.append(result.group(1))
        file.close()

        for subclass in get_subclasses_recursive(Element):
            subclass: Element
            # And another check to ensure no dupes
            assert not (subclass.id in element_ids)
            # And finally making sure that every element ID is in found_element_names
            assert subclass.id in found_element_names
            element_ids.append(subclass.id)
