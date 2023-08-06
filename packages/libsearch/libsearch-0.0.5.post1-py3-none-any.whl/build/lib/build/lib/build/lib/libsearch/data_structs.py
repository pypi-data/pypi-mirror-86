import itertools

class Node():
    def __init__(self, state, parent, action, enable_depth=False):
        self.state = state
        self.parent = parent
        self.action = action
        if enable_depth:
            self.depth = Node.find_depth(self)


    @staticmethod
    def find_depth(node):
        count = 0
        while node.parent is not None:
            count += 1
            node = node.parent
        return count

class HeuristicNode():
    """
    A node that keeps cost attribute too.
    Tracks:
    - cost_from_start: in problems where the cost of the path between two nodes equals to 1 (ex. moving on next tile in a maze)
    - cost: estimated cost to the goal. It will be calculated by a heuristic function
    Used in informed search
    """
    def __init__(self, state, parent, action, cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost_from_start = HeuristicNode.find_depth(self)
        self.cost = cost

    @staticmethod
    def find_depth(node):
        count = 0
        while node.parent is not None:
            count += 1
            node = node.parent
        return count


class WeightNode():
    """
    A node that keeps cost attribute too.
    Tracks:
    - cost_from_start: in problems where the cost is different on each paths. (ex. Weighted graphs)
    """
    def __init__(self, state, parent, action, cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost


    @staticmethod
    def find_depth(node):
        count = 0
        while node.parent is not None:
            count += 1
            node = node.parent
        return count

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def contains_node(self, action, state):
        return any(node.state == state and node.action == action for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

from queue import PriorityQueue
import itertools
from heapq import heappush, heappop
class MyPriorityQueue(PriorityQueue):
    """
    https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
    """

    def _init(self, maxsize):
        self.queue = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count

    
    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = (priority, count, task)
        print("entry: {}".format(entry) )
        self.entry_finder[task] = entry
        heappush(self.queue, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.queue:
            priority, count, task = heappop(self.queue)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')