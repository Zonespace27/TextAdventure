from ._base_test_class import TestClass
from packages.verbs import *
from packages.verbs._verb import Verb
import global_textadv
from re import search
from localization import Localization


class TestClass2(TestClass):
    def test_localization(self):
        self.init_things()
        assert len(Localization.localization_dict) == 0

        global_textadv.selected_language = "unit_testing"
        Localization.generate_localization()

        assert Localization.localize(
            "Unlocalized String") == "Unlocalized String"
        assert Localization.localize("localization.base1") == "Response1"
        assert Localization.localize(
            "localization.base2.inside1") == "Response2"
        assert Localization.localize(
            "localization.base2.inside2.inside^2") == "Response3"
