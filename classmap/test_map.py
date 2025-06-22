from classmap.core import ClassMap

class TestMap:
    def __init__(self, class_map: ClassMap):
        self.base = class_map
        self.class_map = ClassMap()
        self.test = self.mapcreate()
        self.init()

    def mapcreate(self):
        a = ClassMap()
        return a

    def test_map(self):
        self.class_map.parse_directory()
        self.class_map.show_class_info()

    def init(self):
        a = 1
        b = 3
        print(a+b)
        self.test1 = self.mapcreate()
        self.test2 = ClassMap()
