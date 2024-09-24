import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# Load words from words.txt into a list
with open('words_250000_train.txt', 'r') as f:
    words_list = f.read().splitlines()

# Hangman class
class Hangman:
    def __init__(self, word):
        print("New word: ", word, "\n")
        self.word = word
        self.guesses = []
        self.max_attempts = 6
        self.attempts_left = self.max_attempts

    def guess(self, letter):
        self.guesses.append(letter)
        if letter not in self.word:
            self.attempts_left -= 1

    def is_word_guessed(self):
        return all(letter in self.guesses for letter in self.word)

    def get_current_state(self):
        return ''.join([letter if letter in self.guesses else '_' for letter in self.word])

    def get_remaining_attempts(self):
        return self.attempts_left

    def is_game_over(self):
        return self.attempts_left == 0 or self.is_word_guessed()

# DQN Agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.9  # discount factor
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, available_actions):
        if np.random.rand() <= self.epsilon:
            return random.choice(available_actions)
        q_values = self.model.predict(state)
        available_q_values = q_values[0][available_actions]
        return available_actions[np.argmax(available_q_values)]

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state.reshape(1, -1))[0]))
            target_f = self.model.predict(state.reshape(1, -1))
            target_f[0][action] = target
            self.model.fit(state.reshape(1, -1), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# RL Training
def train_rl_agent(words_list, epochs=250000, batch_size=32):
    # Create a dictionary for indexing characters for actions
    chars = sorted(list(set(''.join(words_list))))
    char_to_idx = {char: idx for idx, char in enumerate(chars)}
    idx_to_char = {idx: char for char, idx in char_to_idx.items()}

    state_size = len(chars)
    action_size = len(chars)

    agent = DQNAgent(state_size, action_size)
    random.shuffle(words_list)
    for epoch in range(epochs):
        word=words_list[epoch]
        hangman = Hangman(word)
        done = False

        while not done:
            state = np.array([1 if idx_to_char[idx] in hangman.guesses else 0 for idx in range(state_size)])
            available_actions = [idx for idx in range(len(chars)) if idx_to_char[idx] not in hangman.guesses]
            action = agent.act(state.reshape(1, -1), available_actions)

            letter = idx_to_char[action]
            hangman.guess(letter)

            next_state = np.array([1 if idx_to_char[idx] in hangman.guesses else 0 for idx in range(state_size)])
            reward = -1 if letter not in word else 0
            done = hangman.is_game_over()

            agent.remember(state, action, reward, next_state, done)

        if epoch > batch_size:
            agent.replay(batch_size)

        print(f"Epoch: {epoch + 1}/{epochs}, Word: {word}, Epsilon: {agent.epsilon}")

    return agent

if __name__ == "__main__":
    # Training the RL agent
    trained_agent = train_rl_agent(words_list)

    # Save the trained agent's model
    trained_agent.model.save('hangman_dqn_model.h5')
