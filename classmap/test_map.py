from classmap.core import ClassMap

class TestMap:
    def __init__(self):
        self.class_map = ClassMap()

    def test_map(self):
        self.class_map.parse_directory()
        self.class_map.show_class_info()
