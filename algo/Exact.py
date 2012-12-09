__author__ = 'niyaz'

class Exact(object):

    results = {}

    def __init__(self):
        self.results = {}

    def get_colors_by_graph(self, graph):
        colors = []
        self.get_colors(graph,0,[],0)
        answer = []
        for color_count in range(0,3):
            if color_count in self.results.keys():
                answer = self.results[color_count]
                break
        results = {}
        return answer


    def get_colors(self, graph, vert_number, colors, max_color):
        if max_color > 3:
            return
        if vert_number >= graph.get_vertices_count():
            if max_color not in self.results.keys():
                self.results[max_color] = colors[:]
            return
        for color in range(0,3):
            color_good = True
            for adjacent_vert in range(0,vert_number):
                if graph.is_adjacent_vertices(adjacent_vert,vert_number) and color==colors[adjacent_vert]:
                    color_good = False
            if color_good:
                colors.insert(vert_number,color)
                color_was = max_color
                if max_color < color:
                    max_color = color
                self.get_colors(graph,vert_number+1,colors,max_color)
                max_color = color_was
                colors.pop(vert_number)
