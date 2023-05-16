from json import load

class TestClass():
    def test_unique_object_ids(self):
        found_ids: list[str] = []
        file_locs: list[str] = [ # Once i've got a concrete file structure down, i'll convert this to something better
            'json/objects.json',
        ]
        for file in file_locs:
            data = load(open(file))
            for object_id in data:
                assert not (object_id in found_ids)
                found_ids.append(object_id)
