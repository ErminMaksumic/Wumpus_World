import random
import numpy as np
import csv
import ast

class WumpusGame:
    def __init__(self, size=6):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.agent_pos = (0, 0)
        self.wumpus_pos = None
        self.pit_pos = None
        self.gold_pos = None
        self.arrows = 1
        self.score = 0
        self.game_ended = False
        self.wins = 0
        self.losses = 0
        self.q_table = np.zeros((size, size, 4))  # Q-table for Q-learning

    def initialize_game(self):
        self.agent_pos = (0, 0)
        self.wumpus_pos = self.generate_random_position()
        self.pit_pos = self.generate_random_position()
        self.gold_pos = self.generate_random_position()
        while self.wumpus_pos == self.pit_pos or self.wumpus_pos == self.gold_pos or self.pit_pos == self.gold_pos or self.wumpus_pos == self.agent_pos or self.pit_pos == self.agent_pos or self.gold_pos == self.agent_pos:
            self.pit_pos = self.generate_random_position()
            self.gold_pos = self.generate_random_position()
            self.wumpus_pos = self.generate_random_position()
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
            if not self.game_ended:
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
            self.end_game("Congratulations! You found the gold.", self.score)
        elif self.pit_pos in self.get_adjacent_cells(self.agent_pos):
            self.score -= 10
            print("You feel a cool breeze.")
        elif self.wumpus_pos in self.get_adjacent_cells(self.agent_pos):
            self.score -= 10
            print("You smell a foul stench.")
        elif self.score < -1000:
            self.end_game("Game over!", self.score)

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
        if self.agent_pos == self.gold_pos:
            self.wins += 1
        elif self.score <= -1000:
            self.losses += 1

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

    def update_q_table(self, state, action, next_state, reward, learning_rate, discount_factor):
        x, y = state
        x_next, y_next = next_state

        current_q = self.q_table[x, y, action]
        max_q_next = np.max(self.q_table[x_next, y_next])

        new_q = (1 - learning_rate) * current_q + learning_rate * (reward + discount_factor * max_q_next)
        self.q_table[x, y, action] = new_q

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

    def automate_game(self):
        learning_rate = 0.1
        discount_factor = 0.9
        epsilon = 0.1

        iterations = 1000

                #Read the Q-table from the CSV file
        qtable_loaded = np.loadtxt('qtable.csv', delimiter=',')

        #Reshape the loaded Q-table to the desired shape
        self.q_table = qtable_loaded.reshape((self.size, self.size, 4))        

        for _ in range(iterations):
            self.initialize_game()
            self.display_grid()

            while True:
                state = self.agent_pos

                # Explore or exploit
                if random.random() < epsilon:
                    # Explore: choose a random action
                    action = random.randint(0, 3)  # 0: up, 1: down, 2: left, 3: right
                else:
                    # Exploit: choose the action with the highest Q-value
                    x, y = state
                    q_values = self.q_table[x, y]
                    action = np.argmax(q_values)

                direction = self.get_direction(self.agent_pos, self.get_next_position(action))
                self.move_agent(direction)
                self.display_grid()
                print("Score:", self.score)

                next_state = self.agent_pos
                reward = self.calculate_reward()

                # Update the Q-table
                self.update_q_table(state, action, next_state, reward, learning_rate, discount_factor)

                # Check if the game ended
                if self.game_ended:
                    break

            print("-------------------------------------")
            print("Wins:", self.wins)
            print("Losses:", self.losses)

        #print("Q table", self.q_table)

        np.savetxt('qtable.csv', self.q_table.flatten(), delimiter=',')

    def calculate_reward(self):
        if self.agent_pos == self.gold_pos:
            return 1000
        elif self.agent_pos == self.wumpus_pos or self.agent_pos == self.pit_pos:
            return -1000
        else:
            return -1

    def get_next_position(self, action):
        x, y = self.agent_pos

        if action == 0:  # Up
            return x - 1, y
        elif action == 1:  # Down
            return x + 1, y
        elif action == 2:  # Left
            return x, y - 1
        elif action == 3:  # Right
            return x, y + 1
        else:
            return x, y

def insert_data_into_csv(file_path, data):
    # Open the CSV file in append mode
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the data to the CSV file
        writer.writerow(data)


class CustomObject:
    def __init__(self, iterations, wins, losses,qtable):
        self.iterations = iterations
        self.wins = wins
        self.losses = losses
        self.qtable = qtable

def read_data_from_csv(file_path):
    data = []
     
    # Open the CSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
            
        next(reader)
        # Read each row of data in the CSV file
        for row in reader:
            iterations, wins, losses,qtable = row
            obj = CustomObject(iterations, wins, losses,qtable)
            data.append(obj)
        
    return data


# Testing the game
game = WumpusGame()
game.automate_game()