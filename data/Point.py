__author__ = 'Nikita.Tolstikov'

class Point:
    def __init__(self, x, y):
        self.__x  = x
        self.__y  = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y
    def __str__(self):
        return '({0:f};{1:f})'.format(self.x ,self.y)
    x = property(get_x)
    y = property(get_y)