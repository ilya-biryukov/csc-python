__author__ = 'Nikita.Tolstikov'

import cPickle

class Serializer(object):
    @staticmethod
    def dump_to_file(countries, color_map, filename):
        with open(filename, 'w') as f:
            cPickle.dump((countries, color_map), f)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as f:
            return cPickle.load(f)
