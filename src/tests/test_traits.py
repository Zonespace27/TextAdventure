from base_obj import BaseObj
from traits import TRAIT_LOCKED, TRAIT_SOURCE_UNIT_TESTING_1, TRAIT_SOURCE_UNIT_TESTING_2


class TestClass():
    def test_traits(self):
        new_obj: BaseObj = BaseObj()
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
