from Boards import Board

from heapq import heappop,heappush
import time
import resource

final_board = Board([0,1,2,3,4,5,6,7,8])


class Solver():
    def __init__(self, method, config):
        self.init_board = Board(config)
        self.method = method
        self.nodes_expanded = 0
        self.max_search_depth = 0
        self.path_to_goal = []
        self.cost_of_path = 0
        self.search_depth = 0
        self.running_time = 0.0
        self.max_ram_usage = 0.0

    def solve(self):
        start_time = time.time()
        if self.method == 'bfs':
            final_board = self.bfs(self.init_board)
        elif self.method == 'dfs':
            final_board = self.dfs(self.init_board)
        elif self.method=='ast':
            final_board=self.ast(self.init_board)
        else:
            raise(ValueError('The medtod entered is wrong'))

        self.running_time = time.time() - start_time
        self.max_ram_usage = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 100000000
        self.search_depth = final_board.depth
        self.path_to_goal = Solver.get_path(final_board)
        self.cost_of_path = len(self.path_to_goal)

    def __str__(self):
        s = "path_to_goal: {}\n"  # the sequence of moves taken to reach the goal
        s += "cost_of_path: {}\n"  # the number of moves taken to reach the goal
        s += "nodes_expanded: {}\n"  # the depth within the search tree when the goal node is found
        s += "search_depth: {}\n"
        s += "max_search_depth: {}\n"
        s += "running_time: {}\n"
        s += "max_ram_usage: {}\n"
        s = s.format(self.path_to_goal, self.cost_of_path, self.nodes_expanded, self.search_depth,
                     self.max_search_depth,
                     self.running_time, self.max_ram_usage)
        return s

    def bfs(self, init_board):
        fifo = [init_board]
        visited = set()
        visited.add(init_board)
        while len(fifo) > 0:
            board = fifo.pop(0)
            if board == final_board:
                break
            self.nodes_expanded += 1
            frontier = board.get_frontier()
            for i in frontier:
                if i not in visited:
                    fifo.append(i)
                    visited.add(i)
                    self.max_search_depth = max(self.max_search_depth, i.depth)
        return board

    def dfs(self, init_board):
        lifo = [init_board]
        visited = set()
        visited.add(init_board)
        while len(lifo) > 0:
            board = lifo.pop()
            if board == final_board:
                break
            self.nodes_expanded += 1
            frontier = board.get_frontier()
            for i in reversed(frontier):
                if i not in visited:
                    lifo.append(i)
                    visited.add(i)
                    self.max_search_depth = max(self.max_search_depth, i.depth)
        return board

    def ast(self, init_board):

        heap = []
        heappush(heap,init_board)
        visited = set()
        visited.add(init_board)
        while len(heap) > 0:
            board = heappop(heap)

            if board == final_board:
                break
            self.nodes_expanded += 1
            frontier = board.get_frontier()
            for i in frontier:
                if i not in visited:
                    heappush(heap, i)
                    visited.add(i)
                    self.max_search_depth = max(self.max_search_depth, i.depth)
        return board

    @staticmethod
    def get_path(last_node):
        path = []
        node = last_node
        moves=last_node.moves_dict
        while node.parent is not None:
            path.append(moves[node.generated_by_move])
            node = node.parent
        return list(reversed(path))
