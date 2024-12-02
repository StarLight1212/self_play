# train.py

from agent import PolicyAgent
from game import GameState
from config import Config


def train_self_play(config: Config, save_path: str = 'policy_agent.pkl'):
    agent_X = PolicyAgent('X', config)
    agent_O = PolicyAgent('O', config)

    for episode in range(1, config.episodes + 1):
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
            agent_X.update_policy(states_X, 1)
            agent_O.update_policy(states_O, -1)
        elif winner == 'O':
            agent_X.update_policy(states_X, -1)
            agent_O.update_policy(states_O, 1)
        else:
            agent_X.update_policy(states_X, 0)
            agent_O.update_policy(states_O, 0)

        if episode % 1000 == 0:
            print(f"已完成训练轮数: {episode}/{config.episodes}")

    agent_X.save_policy(save_path)
    print("训练完成，策略已保存。")


if __name__ == "__main__":
    config = Config()
    train_self_play(config)