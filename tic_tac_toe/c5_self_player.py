import pickle
import numpy as np
from c1_mcts_player import GameState, print_board, MCTSNode


class PolicyAgent:
    def __init__(self, player):
        self.player = player
        self.policy = {}   # 策略表

    def choose_action(self, state):
        legal_actions = state.get_legal_actions()
        key = tuple(state.board)
        if key not in self.policy:
            self.policy[key] = np.ones(len(legal_actions)) / len(legal_actions)
        action_probs = self.policy[key]
        action = np.random.choice(legal_actions, p=action_probs)
        return action

    def update_policy(self, states, reward):
        for state in states:
            key = tuple(state.board)
            if key in self.policy:
                self.policy[key] += 0.1 * reward
                total = np.sum(self.policy[key])
                self.policy[key] /= total


def train_self_play(episodes):
    agent_X = PolicyAgent('X')
    agent_O = PolicyAgent('O')
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
            agent_X.update_policy(states_X, 1)
            agent_O.update_policy(states_O, -1)
        elif winner == 'O':
            agent_X.update_policy(states_X, -1)
            agent_O.update_policy(states_O, 1)
        else:
            agent_X.update_policy(states_X, 0)
            agent_O.update_policy(states_O, 0)
    with open('policy_agent.pkl', 'wb') as f:
        pickle.dump(agent_X.policy, f)


def play_self_play():
    with open('policy_agent.pkl', 'rb') as f:
        policy = pickle.load(f)
    agent = PolicyAgent('X')
    agent.policy = policy
    state = GameState()
    while True:
        print_board(state.board)
        if state.current_player == 'X':
            action = agent.choose_action(state)
            state = state.take_action(action)
        else:
            action = int(input("请输入你的动作 (0-8): "))
            if state.board[action] != ' ':
                print("非法动作，请重新输入。")
                continue
            state = state.take_action(action)

        winner = state.get_winner()
        if winner or ' ' not in state.board:
            print_board(state.board)
            if winner:
                print(f"游戏结束，{winner}获胜！")
            else:
                print("平局！")
            break


if __name__ == "__main__":
    # train_self_play(10000)
    play_self_play()
