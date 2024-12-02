from train import train_self_play
from agent import PolicyAgent
from game import GameState
from config import Config
from itertools import product
import pickle


def evaluate_policy(config: Config, episodes: int = 1000) -> float:
    agent_X = PolicyAgent('X', config)
    agent_O = PolicyAgent('O', config)
    win_X = 0
    win_O = 0
    draw = 0

    for _ in range(episodes):
        state = GameState()
        states_X = []
        states_O = []

        while not state.is_terminal():
            if state.current_player == 'X':
                action = agent_X.choose_action(state)
                states_X.append(state)
            else:
                action = agent_O.choose_action(state)
                states_O.append(state)
            state = state.take_action(action)

        winner = state.get_winner()
        if winner == 'X':
            win_X += 1
        elif winner == 'O':
            win_O += 1
        else:
            draw += 1

    win_rate_X = win_X / episodes
    return win_rate_X


def hyperparameter_search():
    learning_rates = [0.05, 0.1, 0.2]
    exploration_rates = [0.05, 0.1, 0.2]
    best_config = None
    best_win_rate = -1

    for lr, er in product(learning_rates, exploration_rates):
        config = Config(learning_rate=lr, exploration_rate=er, episodes=10000)
        print(f"训练配置: learning_rate={lr}, exploration_rate={er}")
        train_self_play(config, 'temp_policy.pkl')
        win_rate = evaluate_policy(config, episodes=1000)
        print(f"评估结果: AI胜率={win_rate * 100:.2f}%")
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            best_config = config

    print(
        f"最佳配置: learning_rate={best_config.learning_rate}, exploration_rate={best_config.exploration_rate}, AI胜率={best_win_rate * 100:.2f}%")


if __name__ == "__main__":
    hyperparameter_search()