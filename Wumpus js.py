import random
from collections import deque

class WumpusGame:
    def __init__(self, size=6):
        self.size = size
        self.grid = [[[] for _ in range(size)] for _ in range(size)]
        self.agent_pos = (0, 0)
        self.wumpus_pos = None
        self.pit_pos = None
        self.gold_pos = None
        self.arrows = 1
        self.score = 0
        self.game_ended = False

    def initialize_game(self):
        self.agent_pos = (0, 0)
        self.wumpus_pos = self.generate_random_position()
        self.pit_pos = self.generate_random_position()
        self.gold_pos = self.generate_random_position()
        while self.wumpus_pos == self.pit_pos or self.wumpus_pos == self.gold_pos or self.pit_pos == self.gold_pos:
            self.pit_pos = self.generate_random_position()
            self.gold_pos = self.generate_random_position()
        self.arrows = 1
        self.score = 0
        self.game_ended = False

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
            if self.game_ended != True:
                self.score -= 1
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
            self.score -= 10
            return True
        return False

    def handle_encounter(self):
        if self.agent_pos == self.wumpus_pos:
            self.score -= 1000
            self.end_game("Game over! You were eaten by the Wumpus.", self.score)
        elif self.agent_pos == self.pit_pos:
            self.score -= 1000
            self.end_game("Game over! You fell into a pit.", self.score)
        elif self.agent_pos == self.gold_pos:
            self.score += 1000
            self.end_game("handle_encounter.Congratulations! You found the gold.", self.score)
        elif self.pit_pos in self.get_adjacent_cells(self.agent_pos):
            print("You feel a cool breeze.")
        elif self.wumpus_pos in self.get_adjacent_cells(self.agent_pos):
            print("You smell a foul stench.")

    def handle_shot(self, pos):
        if pos == self.wumpus_pos:
            print("Congratulations! You shot the Wumpus.")
            self.wumpus_pos = None
            self.score += 1
        else:
            print("You missed.")
            self.move_wumpus()

    def move_wumpus(self):
        adjacent_cells = self.get_adjacent_cells(self.wumpus_pos)
        new_pos = random.choice(adjacent_cells)
        self.wumpus_pos = new_pos
    
    def end_game(self, message, final_score):
        self.display_grid()
        print(message)
        print("Your final score is:", final_score)
        self.game_ended = True

    def display_grid(self):
        print("+" + "-" * (4 * self.size - 1) + "+")
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.agent_pos:
                    print("| A ", end="")
                elif (i, j) == self.wumpus_pos:
                    print("| W ", end="")
                elif (i, j) == self.pit_pos:
                    print("| P ", end="")
                elif (i, j) == self.gold_pos:
                    print("| G ", end="")
                elif (i, j) in self.get_adjacent_cells(self.pit_pos):
                    print("| B ", end="")
                elif (i, j) in self.get_adjacent_cells(self.wumpus_pos):
                    print("| S ", end="")
                else:
                    print("|   ", end="")
            print("|")
            if i != self.size - 1:
                print("|" + "---|" * self.size)
        print("+" + "-" * (4 * self.size - 1) + "+")

    
    def bfs(self):
        # Initialize visited and queue
        visited = set()
        queue = deque()

        # Add the agent's initial position to the queue
        queue.append((self.agent_pos, []))

        while queue:
            position, path = queue.popleft()
            x, y = position

            # Check if the current position is the gold position
            if position == self.gold_pos:
                return path

            # Check if the current position is not visited
            if position not in visited:
                visited.add(position)

                # Add the adjacent cells to the queue
                adjacent_cells = self.get_adjacent_cells(position)
                for adjacent_cell in adjacent_cells:
                    if adjacent_cell not in visited:
                        queue.append((adjacent_cell, path + [adjacent_cell]))

        return None

    def automate_game(self):
        for _ in range(10):
            self.initialize_game()
            self.display_grid()

            while True:
                # Use BFS to find the path to the gold position
                path = self.bfs()

                if path is None:
                    print("No path to the gold position.")
                    break

                # Move the agent along the path
                for position in path:
                    if self.game_ended != True:
                        direction = self.get_direction(self.agent_pos, position)
                        self.move_agent(direction)
                        self.display_grid()
                        print("Score:", self.score)

                    # Check if the agent found the gold or the game ended
                    if self.agent_pos == self.gold_pos:
                        print("Congratulations! You found the gold.")
                        break
                    elif self.score <= -1000:
                        print("Game over! You lost.")
                        break

                # Check if the agent found the gold or the game ended
                if self.agent_pos == self.gold_pos or self.score <= -1000:
                    break

                # Shoot an arrow
                if self.arrows > 0:
                    self.shoot_arrow('up')

                    # Check if the agent found the gold or the game ended
                    if self.agent_pos == self.gold_pos:
                        print("Congratulations! You found the gold.")
                        break
                    elif self.score <= -1000:
                        print("Game over! You lost.")
                        break
            print("-------------------------------------")
        

    def get_direction(self, current_pos, next_pos):
        cx, cy = current_pos
        nx, ny = next_pos

        if cx < nx:
            return 'down'
        elif cx > nx:
            return 'up'
        elif cy < ny:
            return 'right'
        elif cy > ny:
            return 'left'
        else:
            return ''

# Testing the game
game = WumpusGame()
game.automate_game()
