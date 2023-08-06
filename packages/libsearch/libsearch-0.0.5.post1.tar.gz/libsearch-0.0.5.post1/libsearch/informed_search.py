from .data_structs import HeuristicNode, MyPriorityQueue, StackFrontier


def a_star(**kwargs):
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    heuristic = kwargs.get('heuristic', None)
    show_explored = kwargs.get('show_explored', False) #if True it will return the explored(closed) set too.
    count_states = kwargs.get('count_states', False) #if True it will return the number of explored states. num_explored
    

    num_explored = 0
    start = HeuristicNode(state=start, parent=None, action=None, cost=0)
    
    frontier = MyPriorityQueue()
    costs = {}
    frontier.add_task(start, start.cost)
    costs[start] = start.cost
    
    explored = set()
    print("A Star:")
    while True:
        if frontier.empty():
            return None
    
        node = frontier.pop_task()
        #print(node)
        num_explored += 1
        explored.add(node.state)

        if node.state == goal:
            actions_to_goal = []
            states_to_goal = []
            while node.parent is not None:
                actions_to_goal.append(node.action)
                states_to_goal.append(node.state)
                node = node.parent
            actions_to_goal.reverse()
            states_to_goal.reverse()
            solution = (actions_to_goal, states_to_goal)
            if show_explored and count_states:
                return solution, num_explored, explored
            elif show_explored:
                return solution, explored
            elif count_states:
                return solution, num_explored
            else:
                return solution
        print("node state: {} , goal: {}".format(node.state, goal))
        print("Node cost: {}".format(node.cost))
        
        for action, state in actions(node.state):
            if state in explored:
                continue
            child = HeuristicNode(state=state, parent=node, action=action)
            child.cost = child.cost_from_start + heuristic(child.state, goal)
            if child not in costs or  child.cost < costs[child]:
                if child in costs:
                    frontier.remove_task(child)
                costs[child] = child.cost
                frontier.add_task(child, child.cost)


def best_first_search(**kwargs):
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    heuristic = kwargs.get('heuristic', None)
    show_explored = kwargs.get('show_explored', False) #if True it will return the explored(closed) set too.
    count_states = kwargs.get('count_states', False) #if True it will return the number of explored states. num_explored
    

    num_explored = 0
    start = HeuristicNode(state=start, parent=None, action=None, cost=0)
    
    frontier = MyPriorityQueue()
    costs = {}
    frontier.add_task(start, start.cost)
    costs[start] = start.cost
    
    explored = set()
    print("Best First Search:")
    while True:
        if frontier.empty():
            return None
    
        node = frontier.pop_task()
        #print(node)
        num_explored += 1
        explored.add(node.state)

        if node.state == goal:
            actions_to_goal = []
            states_to_goal = []
            while node.parent is not None:
                actions_to_goal.append(node.action)
                states_to_goal.append(node.state)
                node = node.parent
            actions_to_goal.reverse()
            states_to_goal.reverse()
            solution = (actions_to_goal, states_to_goal)
            if show_explored and count_states:
                return solution, num_explored, explored
            elif show_explored:
                return solution, explored
            elif count_states:
                return solution, num_explored
            else:
                return solution
        print("node state: {} , goal: {}".format(node.state, goal))
        print("Node cost: {}".format(node.cost))
        
        for action, state in actions(node.state):
            if state in explored:
                continue
            child = HeuristicNode(state=state, parent=node, action=action)
            #print("Child state: {}".format(child.state))
            #print("goal: {}".format(goal))
            child.cost = heuristic(child.state, goal)
            #print("Child cost: {}".format(child.cost))
            if child not in costs or  child.cost < costs[child]:
                if child in costs:
                    frontier.remove_task(child)
                costs[child] = child.cost
                frontier.add_task(child, child.cost)

from heapq import heappush, heappop
def id_depth_first_search(**kwargs):
    '''
    This dfs implementation is used only for iterative deepening a* below.
    Returns the solution or the new cost limit to be inserted into next dfs search
    '''
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    heuristic = kwargs.get('heuristic', None)
    show_explored = kwargs.get('show_explored', False) #if True it will return the explored(closed) set too.
    depth = kwargs.get('depth', None)   #this is used only when dfs is called in iterative deepening to a certain depth
    
    #print("Depth: {}".format(depth))
    
    num_explored = 0
    

    start = HeuristicNode(state=start, parent=None, action=None, cost=0)

    frontier = StackFrontier()
    frontier.add(start)
    encountered_costs = []
    explored = set()
    print("dfs in informed")
    while True:

        #when the search with the bound of cost finish without solution, returns the new bound which is the minimum from costs greater than current bound.
        if frontier.empty():
            return heappop(encountered_costs)

        node = frontier.remove()
        print('In frontier')
        num_explored += 1

        if node.state == goal:
            actions_to_goal = []
            states_to_goal = []
            while node.parent is not None:
                actions_to_goal.append(node.action)
                states_to_goal.append(node.state)
                node = node.parent
            actions_to_goal.reverse()
            states_to_goal.reverse()
            solution = (actions_to_goal, states_to_goal)
            #print(solution)
            if show_explored:
                return solution, explored
            else:
                return solution
            #return solution

        
        explored.add(node.state)
        if node.cost <= depth:
            for action, state in actions(node.state):
                if not frontier.contains_state(state) and state not in explored:
                    child = HeuristicNode(state=state, parent=node, action=action)
                    child.cost = child.cost_from_start + heuristic(child.state, goal)
                    frontier.add(child)
        else:
            heappush(encountered_costs, node.cost)

def iterative_deepening_a_star(**kwargs):
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    heuristic = kwargs.get('heuristic', None)
    show_explored = kwargs.get('show_explored', False) #if True it will return the explored(closed) set too.
    
    root_node = HeuristicNode(state=start, parent=None, action=None, cost=0)
    depth = root_node.cost
    solution = None
    print("Iterative Deepening with A Star:")
    while True:
        solution = id_depth_first_search(actions=actions, start=start, goal=goal, depth=depth, heuristic=heuristic, show_explored=show_explored)
        if isinstance(solution, int):
            depth  = solution
            print("Depth id: {}".format(depth))
        else:
            break
    #print(solution)
    return solution