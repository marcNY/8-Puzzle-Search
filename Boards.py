import math

class Board:
    moves_dict={0:'Up',1:'Down',2:'Left',3:'Right'}
    def __init__(self, ini_position):
        assert(isinstance(ini_position,list))
        self.state = ini_position
        self.state_dim = math.sqrt(len(self.state))
        self.depth = 0
        self.generated_by_move = ''
        self.parent = None
        if not self.state_dim.is_integer():
            raise (ValueError('The initial state entered is not correct'))
        if 0 not in self.state:
            raise (ValueError('The initial state entered is not correct'))
        self.state_dim = int(self.state_dim)

    @property
    def state_size(self):
        return len(self.state)
    @property
    def heuristic(self):
        return sum([abs(x-self.state.index(x)) for x in self.state if x>0])+self.depth
    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return "Board(" + str(self.state) + ")"

    def __repr__(self):
        return "Board(" + str(self.state) + ")"

    def __hash__(self):
        return hash(tuple(self.state))

    def __lt__(self, other):
        return self.heuristic < other.heuristic

    def move(self, command):
        a = self.state.index(0)
        if command == 0:
            new_index = a - self.state_dim
        elif command == 1:
            new_index = a + self.state_dim
        elif command == 2:
            new_index = a - 1
        elif command == 3:
            new_index = a + 1
        else:
            raise (ValueError("Wrong command entered", command))
        T=list(self.state)
        T[a],T[new_index]=T[new_index],T[a]


        assert(len(T)==9)
        B = Board(T)
        B.depth = self.depth+1
        B.generated_by_move = command
        B.parent = self
        return B

    def get_frontier(self):
        L = []
        boards = []
        a = self.state.index(0)
        if a - self.state_dim >= 0 and self.generated_by_move != 1:
            #L.append('Up')
            boards.append(self.move(0))
        if a + self.state_dim < self.state_size and self.generated_by_move != 0:
            #L.append('Down')
            boards.append(self.move(1))
        if a % self.state_dim != 0 and self.generated_by_move != 3:
            #L.append('Left')
            boards.append(self.move(2))
        if (a + 1) % self.state_dim != 0 and self.generated_by_move != 2:
            #L.append('Right')
            boards.append(self.move(3))
        return boards
        # Board solver using bfs algo
