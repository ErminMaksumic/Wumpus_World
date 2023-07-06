import random

class WumpusGame:
    def __init__(self, size=6):
        self.size = size
        self.grid = [[[] for _ in range(size)] for _ in range(size)]
        self.agent_pos = (0, 0)
        self.wumpus_pos = None
        self.pit_pos = None
        self.gold_pos = None
        self.arrows = 1

    def initialize_game(self):
        self.agent_pos = (0, 0)
        self.wumpus_pos = self.generate_random_position()
        self.pit_pos = self.generate_random_position()
        self.gold_pos = self.generate_random_position()
        while self.wumpus_pos == self.pit_pos or self.wumpus_pos == self.gold_pos or self.pit_pos == self.gold_pos:
            self.pit_pos = self.generate_random_position()
            self.gold_pos = self.generate_random_position()
        self.arrows = 1

    def generate_random_position(self):
        return random.randint(0, self.size - 1), random.randint(0, self.size - 1)

    def get_adjacent_cells(self, pos):
        x, y = pos
        adjacent_cells = []
        if x > 0:
            adjacent_cells.append((x - 1, y))
        if x < self.size - 1:
            adjacent_cells.append((x + 1, y))
        if y > 0:
            adjacent_cells.append((x, y - 1))
        if y < self.size - 1:
            adjacent_cells.append((x, y + 1))
        return adjacent_cells

    def is_valid_move(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size

    def move_agent(self, direction):
        x, y = self.agent_pos
        if direction == 'up':
            new_pos = (x - 1, y)
        elif direction == 'down':
            new_pos = (x + 1, y)
        elif direction == 'left':
            new_pos = (x, y - 1)
        elif direction == 'right':
            new_pos = (x, y + 1)
        else:
            return False

        if self.is_valid_move(new_pos):
            self.agent_pos = new_pos
            self.handle_encounter()
            return True
        return False

    def shoot_arrow(self, direction):
        if self.arrows <= 0:
            print("You have no arrows left.")
            return False

        self.arrows -= 1
        x, y = self.agent_pos
        if direction == 'up':
            pos = (x - 1, y)
        elif direction == 'down':
            pos = (x + 1, y)
        elif direction == 'left':
            pos = (x, y - 1)
        elif direction == 'right':
            pos = (x, y + 1)
        else:
            return False

        if self.is_valid_move(pos):
            self.handle_shot(pos)
            return True
        return False

    def handle_encounter(self):
        x, y = self.agent_pos
        if self.agent_pos == self.wumpus_pos:
            print("Game over! You were eaten by the Wumpus.")
            self.initialize_game()
        elif self.agent_pos == self.pit_pos:
            print("Game over! You fell into a pit.")
            self.initialize_game()
        elif self.agent_pos == self.gold_pos:
            print("Congratulations! You found the gold.")
            self.initialize_game()
        elif self.pit_pos in self.get_adjacent_cells(self.agent_pos):
            print("You feel a cool breeze.")

    def handle_shot(self, pos):
        if pos == self.wumpus_pos:
            print("Congratulations! You shot the Wumpus.")
            self.wumpus_pos = None
        else:
            print("You missed.")
            self.move_wumpus()

    def move_wumpus(self):
        adjacent_cells = self.get_adjacent_cells(self.wumpus_pos)
        new_pos = random.choice(adjacent_cells)
        self.wumpus_pos = new_pos

    def display_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.agent_pos:
                    print("A", end="\t")
                elif (i, j) == self.wumpus_pos:
                    print("W", end="\t")
                elif (i, j) == self.pit_pos:
                    print("P", end="\t")
                elif (i, j) == self.gold_pos:
                    print("G", end="\t")
                elif (i, j) in self.get_adjacent_cells(self.pit_pos):
                    print("B", end="\t")
                else:
                    print("-", end="\t")
            print()

# Testing the game
game = WumpusGame()
game.initialize_game()
game.display_grid()

while True:
    action = input("Enter your action (move: up, down, left, right; shoot: shoot up, shoot down, shoot left, shoot right): ")
    action = action.lower().split()

    if len(action) == 2 and action[0] == 'shoot':
        if game.shoot_arrow(action[1]):
            game.display_grid()
        else:
            print("Invalid action. Try again.")
    elif len(action) == 1 and action[0] in ['up', 'down', 'left', 'right']:
        if game.move_agent(action[0]):
            game.display_grid()
        else:
            print("Invalid action. Try again.")
    else:
        print("Invalid action. Try again.")
