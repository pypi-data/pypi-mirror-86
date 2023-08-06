myGraph = {'A': {'B':8, 'C':5, 'D':10, 'E':8},
        'B': {'A':8, 'C':7, 'D':6, 'E':6},
        'C': {'A':5, 'B':7, 'D':9, 'E':3},
        'D': {'A':10, 'B':6, 'C':9, 'E':4},
        'E': {'A':8, 'B':6, 'C':3, 'D':4}}

class Graph():

    def __init__(self, graph_dict=None):
        self.graph_dict = graph_dict or {}
    

    def path_cost(self, a, b):
        children = self.graph_dict.get(a)
        return children.get(b)
    #print(path_cost('A', 'E')) #should return 8


    def neighbors(self, node):
        """
        returns a list with elements pairs of actions and children of the node.
        ex. [('D-A', 'A'), ('D-B', 'B'), ('D-C', 'C'), ('D-E', 'E')]
        ex. The action D-A thus moving from D to A resulted to state 'A'
        """
        children = self.graph_dict.get(node) #returns the dict in the value of key: node
        result = []
        for child in children:
            result.append((node + '-' + child, child)) 
        return result
    #print(neighbors('D')) #returns list: [('D-A', 'A'), ('D-B', 'B'), ('D-C', 'C'), ('D-E', 'E')]

    def fullneighbors(self, action, state):
        """
        generation actions-states for Full Weighted Graphs ex. TSP: Traveling Salesman Problem
        ex. The state 'A' from action 'D-A' will generate children (tuples represent action that led to state (action, state) ):
            [('D-A-B', 'B'), ('D-A-C', 'C'), ('D-A-E', 'E')]
        ex2. The state 'D' from action 'A-B-C-E-D' will generate only one child - return to initial state:
             [('A-B-C-E-D-A', 'A')]
        """
        vertices = list(self.graph_dict)
        children = self.graph_dict.get(state)
        if action:
            #print("action")
            previous_visited = action.split('-')
            if len(previous_visited) == len(vertices): #if prior actions contains all state, thus visited once.
                previous_visited = previous_visited[1:] #remove first(source) to allow the generation of child to return on it
            #print("previous: {}".format(previous_visited))
            result = []
            for child in children:
                if child not in previous_visited:
                    result.append((action + '-' + child, child))
            return result
        else:
            result = []
            for child in children:
                result.append((state + '-' + child, child)) 
            return result


g = Graph(myGraph)
#print(g.path_cost('A', 'E')) #should return 8
#print(g.neighbors('D')) #returns list: ['A', 'B', 'C', 'E']
#print(g.fullneighbors('D-A','A')) # returns list: [('D-A-B', 'B'), ('D-A-C', 'C'), ('D-A-E', 'E')]
#print(g.fullneighbors('A-B-C-E-D','D')) # returns list [('A-B-C-E-D-A', 'A')]
#print(g.fullneighbors('A-B', 'B'))

from libsearch import branch_and_bound
def test_bb():
    assert branch_and_bound(actions=g.fullneighbors, start='A', goal='A', path_cost=g.path_cost) == (['A-B', 'A-B-D', 'A-B-D-E', 'A-B-D-E-C', 'A-B-D-E-C-A'], ['B', 'D', 'E', 'C', 'A'])