from dataclasses import dataclass


@dataclass
class Config:
    learning_rate: float = 0.05  # 策略更新的学习率
    exploration_rate: float = 0.2  # ε-贪婪策略中的ε值
    episodes: int = 10000  # 训练的总轮数
    discount_factor: float = 1.0  # 折扣因子（暂时未使用）