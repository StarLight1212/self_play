from c1_mcts_player import GameState, print_board
import numpy as np
import pickle

class QLearningAgent:
    def __init__(self, player, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.Q = {}                 # Q表，用于存储状态-动作值
        self.alpha = alpha          # 学习率，控制学习的速度
        self.gamma = gamma          # 折扣因子，衡量未来奖励的重要性
        self.epsilon = epsilon      # 探索率，决定探索新动作的概率
        self.player = player        # 当前玩家，'X' 或 'O'

    def get_Q(self, state, action):
        key = (tuple(state.board), action)  # 将状态和动作组合成键
        return self.Q.get(key, 0.0)          # 返回Q值，如果没有则返回0.0

    def choose_action(self, state):
        legal_actions = state.get_legal_actions()  # 获取当前状态下的合法动作
        if np.random.rand() < self.epsilon:        # 根据探索率决定是否随机选择动作
            return np.random.choice(legal_actions)  # 随机选择一个合法动作
        Qs = [self.get_Q(state, a) for a in legal_actions]  # 获取所有合法动作的Q值
        max_Q = max(Qs)                             # 找到最大Q值
        if Qs.count(max_Q) > 1:                     # 如果有多个动作的Q值相同
            best_actions = [a for a, q in zip(legal_actions, Qs) if q == max_Q]  # 找到所有最佳动作
            return np.random.choice(best_actions)   # 随机选择一个最佳动作
        else:
            return legal_actions[Qs.index(max_Q)]   # 返回Q值最大的动作

    def learn(self, state, action, reward, next_state):
        current_Q = self.get_Q(state, action)  # 获取当前状态和动作的Q值
        next_max_Q = max([self.get_Q(next_state, a) for a in next_state.get_legal_actions()], default=0)  # 获取下一个状态的最大Q值
        new_Q = current_Q + self.alpha * (reward + self.gamma * next_max_Q - current_Q)  # 更新Q值
        key = (tuple(state.board), action)  # 将状态和动作组合成键
        self.Q[key] = new_Q  # 更新Q表中的Q值


def train_q_learning(episodes):
    agent = QLearningAgent('X')
    for _ in range(episodes):
        state = GameState()
        while not state.is_terminal():
            action = agent.choose_action(state)
            next_state = state.take_action(action)
            winner = next_state.get_winner()
            if winner == agent.player:
                reward = 1
            elif winner is not None:
                reward = -1
            else:
                reward = 0
            agent.learn(state, action, reward, next_state)
            state = next_state
    with open('q_table.pkl', 'wb') as f:
        pickle.dump(agent.Q, f)


def play_q_learning():
    with open('q_table.pkl', 'rb') as f:
        Q = pickle.load(f)
    agent = QLearningAgent('X')
    agent.Q = Q
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
    train_q_learning(100000)
    play_q_learning()
