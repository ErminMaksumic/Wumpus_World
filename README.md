# Machine Learning | Artificial Inteligence

The paper discusses the implementation of artificial intelligence (AI) and machine learning (ML) in the context of the Wumpus World game, a classic AI problem where an agent navigates a maze filled with hazards like pits, the Wumpus monster, and a hidden treasure. The primary goal is to train the agent to find the treasure while avoiding dangers using Q-learning, a reinforcement learning technique.

Key points include:

- Q-Learning Table: The agent uses a Q-table to store and update values representing the expected rewards for actions in specific states. This helps the agent learn optimal strategies over time.

- Implementation: The paper details the code for updating the Q-table and automating the game, including parameters like learning rate, discount factor, and epsilon (for exploration vs. exploitation).

- Data Storage and Reuse: The Q-table data is saved and reloaded between iterations to allow the agent to build on previous learning, significantly improving performance over time.

- Results: The agent's performance improves with each iteration, with win rates increasing from 47% in the first iteration to over 96% in later iterations.

Future Work: Suggestions for improvement include using advanced algorithms like Deep Q-Learning, optimizing parameters, and adding more complexity to the game (e.g., multiple agents, traps, and maps).

The paper concludes that even simple games like Wumpus World can effectively demonstrate the power of AI and ML, showing how agents can learn and improve their decision-making over time.