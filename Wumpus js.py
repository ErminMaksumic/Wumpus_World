import random

ROWS = 5
COLS = 6

WUMPUS = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
GOLD = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
PIT1 = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
PIT2 = (random.randint(0, ROWS-1), random.randint(0, COLS-1))

class WumpusWorld:
    def __init__(self):
        self.grid = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
        self.agent_location = (0, 0)
        self.agent_alive = True
        self.agent_won = False
        self.game_over = False

    def print_grid(self):
        for row in self.grid:
            print('+---+---+---+---+---+---+')
            print('| {} | {} | {} | {} | {} | {} |'.format(*row))
        print('+---+---+---+---+---+---+')

    def update_grid(self):
        self.grid = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
        self.grid[WUMPUS[0]][WUMPUS[1]] = 'W'
        self.grid[GOLD[0]][GOLD[1]] = 'G'
        self.grid[PIT1[0]][PIT1[1]] = 'P'
        self.grid[PIT2[0]][PIT2[1]] = 'P'
        self.grid[self.agent_location[0]][self.agent_location[1]] = 'A'

    def move_agent(self, direction):
        if self.game_over:
            print("Igra je završena.")
            return

        row, col = self.agent_location

        if direction == 'up' and row > 0:
            self.agent_location = (row - 1, col)
        elif direction == 'down' and row < ROWS - 1:
            self.agent_location = (row + 1, col)
        elif direction == 'left' and col > 0:
            self.agent_location = (row, col - 1)
        elif direction == 'right' and col < COLS - 1:
            self.agent_location = (row, col + 1)

        self.check_environment()

    def check_environment(self):
        if self.agent_location == WUMPUS and self.agent_alive:
            self.agent_alive = False
            self.game_over = True
            print("Agent je umro. Igra je završena.")
        elif self.agent_location == GOLD and self.agent_alive:
            self.agent_won = True
            self.game_over = True
            print("Agent je pronašao zlato. Pobijedio je!")
        elif self.agent_location == PIT1 or self.agent_location == PIT2:
            self.agent_alive = False
            self.game_over = True
            print("Agent je pao u jamu. Igra je završena.")

        self.update_grid()

    def find_path_dfs(self):
        visited = set()
        path = []
        self.dfs(self.agent_location, visited, path)
        return path

    def dfs(self, current_location, visited, path):
        if current_location == GOLD:
            return True

        visited.add(current_location)

        neighbors = self.get_valid_neighbors(current_location)
        for neighbor in neighbors:
            if neighbor not in visited:
                path.append(neighbor)
                if self.dfs(neighbor, visited, path):
                    return True
                path.pop()

        return False

    def get_valid_neighbors(self, location):
        row, col = location
        neighbors = []

        if row > 0:
            neighbors.append((row - 1, col))
        if row < ROWS - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < COLS - 1:
            neighbors.append((row, col + 1))

        return neighbors

    def automate_moves(self):
        if self.game_over:
            print("Igra je završena.")
            return

        path = self.find_path_dfs()

        for next_location in path:
            self.agent_location = next_location
            self.check_environment()

            if self.game_over:
                break

            self.print_grid()

game = WumpusWorld()
game.update_grid()

while not game.game_over:
    game.print_grid()

    automate = input("Automatski pokreti? (da/ne): ")
    if automate.lower() == 'da':
        game.automate_moves()
    else:
        move = input("Unesite potez (up/down/left/right): ")
        game.move_agent(move)
