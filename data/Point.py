__author__ = 'Nikita.Tolstikov'

class Point:
    def __init__(self, coordinates):
        self.__x  = coordinates[0]
        self.__y  = coordinates[1]

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    x = property(get_x)
    y = property(get_y)