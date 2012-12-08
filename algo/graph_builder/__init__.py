__author__ = 'Man'

import shapefile

reader = shapefile.Reader('WORLD_MAP/WORLD_MAP')
sr = reader.shapeRecords()
for i in xrange(len(sr)):
    print sr[i].record[4]
#    for part in sr[i].shape.parts:
#        print part

#for point in sr[0].shape.points:
#    print point