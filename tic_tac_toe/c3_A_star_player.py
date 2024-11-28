from c1_mcts_player import GameState, print_board
import heapq
import random


def heuristic(state, player):
    # 简单启发式：返回0，表示为BFS
    return 0


def a_star_search(state, player):
    frontier = []
    heapq.heappush(frontier, (heuristic(state, player), state))
    explored = set()
    while frontier:
        _, current_state = heapq.heappop(frontier)
        if current_state.is_terminal():
            return current_state.last_move
        explored.add(tuple(current_state.board))
        for action in current_state.get_legal_actions():
            child_state = current_state.take_action(action)
            if tuple(child_state.board) not in explored:
                heapq.heappush(frontier, (heuristic(child_state, player), child_state))
    return None


def play_a_star():
    state = GameState()
    while True:
        print_board(state.board)
        if state.current_player == 'X':
            action = a_star_search(state, 'X')
            if action is None:
                action = random.choice(state.get_legal_actions())
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
    play_a_star()
