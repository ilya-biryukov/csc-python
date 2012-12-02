__author__ = 'niyaz'

class Exact(object):

    results = {}

    def __init__(self, results):
        self.results = results

    def getColorsByGraph(self, graph):
        colors = []
        self.getColors(graph,0,[],0)
        answer = []
        for colorCount in range(0,3):
            if (self.results.keys().__contains__(colorCount)):
                answer = self.results[colorCount]
                break
        resuts = {}
        return answer


    def getColors(self, graph, vertNumber, colors, maxColor):
        if (maxColor > 3):
            return ;
        if (vertNumber >= graph.get_vertices_count()):
            if (not self.results.keys().__contains__(maxColor)):
                self.results[maxColor] = colors[:]
            return ;
        for color in range(0,3):
            colorGood = True
            for adjacentVert in range(0,vertNumber):
                if (graph.is_adjacent_vertices(adjacentVert,vertNumber) and color==colors[adjacentVert]):
                    colorGood = False
            if (colorGood):
                colors.insert(vertNumber,color)
                colorWas = maxColor
                if (maxColor < color):
                    maxColor = color
                self.getColors(graph,vertNumber+1,colors,maxColor)
                maxColor = colorWas
                colors.pop(vertNumber)
