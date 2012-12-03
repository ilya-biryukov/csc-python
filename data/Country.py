__author__ = 'Nikita.Tolstikov'
class Country(object):
    def __init__(self, country_name, polygons):
        self.__polygons = polygons
        self.__name = country_name

    def get_name(self):
        return self.__name

    def get_polygons(self):
        return self.__polygons


    name = property(get_name)
    polygons = property(get_polygons)