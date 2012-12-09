from data import shapefile
import Builder
__author__ = 'Man'

reader = shapefile.Reader('WORLD_MAP/WORLD_MAP')
sr = reader.shapeRecords()
for i in xrange(len(sr)):
    if sr[i].record[4] != 'Spain' and sr[i].record[4] != 'Portugal':
        continue
    print sr[i].record[4]
    print '---------------------'
    for j in xrange(sr[i].shape.parts[-1], len(sr[i].shape.points)):
        print sr[i].shape.points[j]

#for point in sr[0].shape.points:
#    print point