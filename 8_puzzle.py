import random
import itertools
import collections
import time

class Node:
    """
    A class representing an Solver node
    - 'puzzle' é a instância 
    - 'parent' nó gerado pelo solver, se houver
    - 'action' ação tomada para o quebra-cabeça, se houver
    """
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        if (self.parent != None):
            self.g = parent.g + 1
        else:
            self.g = 0

    @property
    def score(self):
        return (self.g + self.h)

    @property
    def state(self):
        
        return str(self)

    @property 
    def path(self):
        """
        reconstroí um caminho para "parent"
        """
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self):
        """ verifica se é soluvel """
        return self.puzzle.solved

    @property
    def actions(self):
        """ verifica ações para a situação atual """
        return self.puzzle.actions

    @property
    def h(self):
        """"h"""
        return self.puzzle.manhattan

    @property
    def f(self):
        """"f"""
        return self.h + self.g

    def __str__(self):
        return str(self.puzzle)

class Solver:
    """
    um solucionador '8-puzzle' solver
    - 'start' é uma instância Puzzle 
    """
    def __init__(self, start):
        self.start = start

    def solve(self):
        """
        Executa a primeira pesquisa em largura e retorna um 
        caminho, se houver
        """
        queue = collections.deque([Node(self.start)])
        seen = set()
        seen.add(queue[0].state)
        while queue:
            queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
            node = queue.popleft()
            if node.solved:
                return node.path

            for move, action in node.actions:
                child = Node(move(), node, action)

                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)

class Puzzle:
    """
    Classe que representa '8-puzzle'.
    - 'board' deve ser uma lista quadrada com entradas inteiras 0...width^2 - 1
       e.g. [[1,2,3],[4,0,6],[7,5,8]]
    """
    def __init__(self, board):
        self.width = len(board[0])
        self.board = board

    @property
    def solved(self):
        """
        The puzzle é resolvido se os números postos em ordem crescente,
        da direita para a esqueda, e o 0 estiver na última posição
        """
        N = self.width * self.width
        return str(self) == ''.join(map(str, range(1,N))) + '0'

    @property 
    def actions(self):
        """
        Retorna uma lista de 'move', 'action', de forma conjunta. 
        'move' é chamado por um novo puzzle, em que o resulta
        em mover a peça '0' em direção a 'action'
        """
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'Direita':(i, j-1),
                      'Esquerda':(i, j+1),
                      'Baixo':(i-1, j),
                      'Cima':(i+1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                   self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move)
        return moves

    @property
    def manhattan(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j]-1, 3)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def shuffle(self):
        """
        Retorna um novo puzzle que foi embaralhado em mais de 
        1000 movimentos aleatórios
        """
        puzzle = self
        for _ in range(1000):
            puzzle = random.choice(puzzle.actions)[0]()
        return puzzle

    def copy(self):
        """
        Returna um novo puzzle com o mesmo tabuleiro que 'self'
        """
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def _move(self, at, to):
        """
        Returna um novo puzzle quando 'at' e 'to'
        forem trocados.
        NOTE: todos os movimentos devem ser 'actions' que foram executadas
        """
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def pprint(self):
        for row in self.board:
            print(row)
        print()

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row


# example de uso     
board = [[5,2,8],[4,1,7],[0,3,6]]
puzzle = Puzzle(board)
#puzzle = puzzle.shuffle()
s = Solver(puzzle)
tic = time.process_time()
p = s.solve()
toc = time.process_time()

steps = 0
for node in p:
    print(node.action)
    node.puzzle.pprint()
    steps += 1

print("Total de passos: " + str(steps))
print("Tempo gasto na pesquisa: " + str(toc - tic) + " em segundos")