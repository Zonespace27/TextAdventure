from ._base_test_class import TestClass
from base_obj import BaseObj
from base_obj import new_object
from traits import TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_1, TRAIT_SOURCE_UNIT_TESTING_2


class TestClass2(TestClass):
    def test_traits(self):
        self.init_things()
        new_obj: BaseObj = new_object(BaseObj)
        new_obj.add_trait(TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_1)

        assert new_obj.has_trait(TRAIT_LOCKED)
        assert new_obj.has_trait_from(
            TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_1)

        new_obj.add_trait(TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_2)

        assert new_obj.has_trait_from(
            TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_1)
        assert new_obj.has_trait_from(
            TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_2)

        new_obj.remove_trait(TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_1)

        assert not new_obj.has_trait_from(
            TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_1)
        assert new_obj.has_trait_from(
            TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_2)

        new_obj.add_trait(TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_1)
        new_obj.force_remove_trait(TRAIT_LOCKED)

        assert not new_obj.has_trait(TRAIT_LOCKED)
