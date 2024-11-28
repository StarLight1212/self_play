import pickle
import random
import copy
from c1_mcts_player import GameState, print_board, MCTSNode


def hybrid_mcts_q(state, itermax, beam_width):
    root_node = MCTSNode(state)

    for _ in range(itermax):
        node = root_node
        state_copy = copy.deepcopy(state)

        # Selection
        while node.is_fully_expanded() and not state_copy.is_terminal():
            node = node.best_child()
            action = node.state.last_move
            state_copy = state_copy.take_action(action)

        # Expansion
        if not state_copy.is_terminal():
            actions = state_copy.get_legal_actions()
            action_scores = []
            for action in actions:
                q_value = Q.get((tuple(state_copy.board), action), 0.0)
                action_scores.append((q_value, action))
            best_actions = sorted(action_scores, key=lambda x: x[0], reverse=True)[:beam_width]
            for _, action in best_actions:
                new_state = state_copy.take_action(action)
                child_node = MCTSNode(new_state, parent=node)
                child_node.state.last_move = action
                node.children.append(child_node)
            node = random.choice(node.children)
            state_copy = node.state

        # Simulation
        while not state_copy.is_terminal():
            action = random.choice(state_copy.get_legal_actions())
            state_copy = state_copy.take_action(action)

        # Backpropagation
        winner = state_copy.get_winner()
        while node is not None:
            node.visits += 1
            if node.state.current_player == winner:
                node.wins += 1
            node = node.parent

    return sorted(root_node.children, key=lambda c: c.visits)[-1].state.last_move


def play_hybrid():
    with open('q_table.pkl', 'rb') as f:
        global Q
        Q = pickle.load(f)
    state = GameState()
    while True:
        print_board(state.board)
        if state.current_player == 'X':
            action = hybrid_mcts_q(state, 1000, beam_width=2)
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
    play_hybrid()
