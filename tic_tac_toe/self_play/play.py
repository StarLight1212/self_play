# play.py

from agent import PolicyAgent
from game import GameState, print_board
from config import Config


def play_self_play(policy_path: str = 'policy_agent.pkl'):
    config = Config()
    agent = PolicyAgent('X', config)
    agent.load_policy(policy_path)

    state = GameState()
    while True:
        print_board(state.board)
        if state.current_player == 'X':
            action = agent.choose_action(state)
            print(f"AI选择动作: {action}")
            state = state.take_action(action)
        else:
            try:
                action = int(input("请输入你的动作 (0-8): "))
                if state.board[action] != ' ':
                    print("非法动作，请重新输入。")
                    continue
                state = state.take_action(action)
            except (IndexError, ValueError):
                print("输入无效，请输入0到8之间的整数。")
                continue

        winner = state.get_winner()
        if winner or ' ' not in state.board:
            print_board(state.board)
            if winner:
                print(f"游戏结束，{winner}获胜！")
            else:
                print("游戏结束，平局！")
            break


if __name__ == "__main__":
    play_self_play()