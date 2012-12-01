__author__ = 'Man'
import shapefile

reader = shapefile.Reader('WORLD_MAP/WORLD_MAP')
sr = reader.shapeRecords()
print sr[0].record[4]
for part in sr[0].shape.parts:
    print part

for point in sr[0].shape.points:
    print point