import global_textadv
from exception import NoLocalizationLanguage, StringNotLocalized
from json import load


class Localization:
    # Schema Example: Input "localization.dialogue.phone_chat.1" Output "Test"
    # This type isn't precisely correct but I can't do better than this I think
    localization_dict: dict[str, str] = {}

    @staticmethod
    def generate_localization():
        if not global_textadv.selected_language:
            raise NoLocalizationLanguage

        localization_file = open(global_textadv.resource_path(
            f'json/localization/{global_textadv.selected_language}.json'))
        localization_json = load(localization_file)
        Localization.recursive_localization_search(localization_json)

    @staticmethod
    def recursive_localization_search(json_tree, path="localization."):
        for entry in json_tree:
            if isinstance(json_tree[entry], dict):
                path += f"{entry}."
                Localization.recursive_localization_search(
                    json_tree[entry], path)
            elif isinstance(json_tree[entry], str):
                final_path = path + entry
                Localization.localization_dict[final_path] = json_tree[entry]

    @staticmethod
    def localize(input_string: str) -> str:
        if (input_string[0:12] != "localization."):
            if global_textadv.ERROR_NONLOCALIZED:
                raise StringNotLocalized
            return input_string

        return Localization.localization_dict[input_string]
