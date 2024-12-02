import pickle
import numpy as np
from game import GameState, print_board
from config import Config
from dataclasses import dataclass
from typing import List, Tuple, Dict
import random


@dataclass
class PolicyAgent:
    player: str
    config: Config
    policy: Dict[Tuple[str, ...], np.ndarray]

    def __init__(self, player: str, config: Config):
        self.player = player
        self.config = config
        self.policy = {}  # 策略表，键为状态，值为动作概率分布

    def choose_action(self, state: GameState) -> int:
        legal_actions = state.get_legal_actions()
        key = tuple(state.board)

        if key not in self.policy:
            # 初始化动作为均匀分布
            self.policy[key] = np.ones(len(legal_actions)) / len(legal_actions)

        action_probs = self.policy[key]

        # ε-贪婪策略
        if random.random() < self.config.exploration_rate:
            action = random.choice(legal_actions)
        else:
            action = np.random.choice(legal_actions, p=action_probs)

        return action

    def update_policy(self, states: List[GameState], reward: float):
        for state in states:
            key = tuple(state.board)
            if key in self.policy:
                # 更新策略概率
                self.policy[key] += self.config.learning_rate * reward
                # 归一化
                total = np.sum(self.policy[key])
                if total > 0:
                    self.policy[key] /= total
                else:
                    # 防止概率全为零，重新均匀分布
                    self.policy[key] = np.ones_like(self.policy[key]) / len(self.policy[key])

    def save_policy(self, filepath: str):
        with open(filepath, 'wb') as f:
            pickle.dump(self.policy, f)

    def load_policy(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.policy = pickle.load(f)