# twenty_four.py

import itertools
import operator

def calculate_24(nums):
    ops = [operator.add, operator.sub, operator.mul, operator.truediv]
    op_symbols = ['+', '-', '*', '/']
    for num_perm in itertools.permutations(nums):
        for ops_perm in itertools.product(ops, repeat=3):
            for i in range(3):
                try:
                    result = ops_perm[0](num_perm[0], num_perm[1])
                    result = ops_perm[1](result, num_perm[2])
                    result = ops_perm[2](result, num_perm[3])
                    if abs(result - 24) < 1e-6:
                        expression = f"(({num_perm[0]} {op_symbols[ops.index(ops_perm[0])]} {num_perm[1]}) {op_symbols[ops.index(ops_perm[1])]} {num_perm[2]}) {op_symbols[ops.index(ops_perm[2])]} {num_perm[3]}"
                        return expression
                except ZeroDivisionError:
                    continue
    return None

def play_twenty_four():
    while True:
        try:
            nums = list(map(int, input("Enter four numbers separated by spaces: ").split()))
            if len(nums) != 4:
                print("Please enter exactly four numbers.")
                continue
            solution = calculate_24(nums)
            if solution:
                print(f"Solution: {solution} = 24")
            else:
                print("No solution found.")
        except ValueError:
            print("Invalid input. Please enter integers only.")

if __name__ == "__main__":
    play_twenty_four()
