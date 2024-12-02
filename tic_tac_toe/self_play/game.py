import copy
import random
import math


class GameState:
    def __init__(self):
        self.board = [' '] * 9      # 初始空棋盘
        self.current_player = 'X'   # 当前玩家

    def get_legal_actions(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def take_action(self, action):
        new_state = copy.deepcopy(self)
        new_state.board[action] = self.current_player
        new_state.current_player = 'O' if self.current_player == 'X' else 'X'
        return new_state

    def is_terminal(self):
        return self.get_winner() is not None or ' ' not in self.board

    def get_winner(self):
        winning_combinations = [
            (0,1,2), (3,4,5), (6,7,8),    # Rows
            (0,3,6), (1,4,7), (2,5,8),    # Columns
            (0,4,8), (2,4,6)              # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
        return None


def mcts(root_state, itermax):
    root_node = MCTSNode(root_state)

    for _ in range(itermax):
        node = root_node
        state = copy.deepcopy(root_state)

        # Selection
        while node.is_fully_expanded() and not state.is_terminal():
            node = node.best_child()
            action = node.state.last_move
            state = state.take_action(action)

        # Expansion
        if not state.is_terminal():
            for action in state.get_legal_actions():
                new_state = state.take_action(action)
                child_node = MCTSNode(new_state, parent=node)
                child_node.state.last_move = action
                node.children.append(child_node)

            node = random.choice(node.children)
            state = node.state

        # Simulation
        while not state.is_terminal():
            action = random.choice(state.get_legal_actions())
            state = state.take_action(action)

        # Backpropagation
        winner = state.get_winner()
        while node is not None:
            node.visits += 1
            if (node.state.current_player == winner):
                node.wins += 1
            node = node.parent

    return sorted(root_node.children, key=lambda c: c.visits)[-1].state.last_move


def print_board(board):
    symbols = [' ' if s == ' ' else s for s in board]
    print(f"{symbols[0]}|{symbols[1]}|{symbols[2]}")
    print("-+-+-")
    print(f"{symbols[3]}|{symbols[4]}|{symbols[5]}")
    print("-+-+-")
    print(f"{symbols[6]}|{symbols[7]}|{symbols[8]}")


def play_mcts():
    state = GameState()
    while True:
        print_board(state.board)
        if state.current_player == 'X':
            print("AI正在思考...")
            action = mcts(state, 1000)
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