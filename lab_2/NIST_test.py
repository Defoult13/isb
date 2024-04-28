import json
import os
import math

def bit_frequency_test(sequence):
    transformed_sequence = [1 if bit == '1' else -1 for bit in sequence]
    Sn = sum(transformed_sequence) / math.sqrt(len(sequence))
    P_value = math.erfc(Sn / math.sqrt(2))
    return P_value

def consecutive_bit_test(sequence):
    n = len(sequence)
    y = sum(int(bit) for bit in sequence) / n
    if abs(y - 1/2) >= 2 / math.sqrt(n):
        return 0
    Vn = sum(1 for i in range(n - 1) if sequence[i] != sequence[i + 1])
    P_value = math.erfc(abs(Vn - 2 * n * y * (1 - y)) / (2 * math.sqrt(2 * n) * y * (1 - y)))
    return P_value

def longest_run_of_ones_test(sequence, block_size=8):
    n = len(sequence)
    blocks = [sequence[i:i+block_size] for i in range(0, n, block_size)]
    V = [0, 0, 0, 0]  # V1, V2, V3, V4
    for block in blocks:
        max_run_length = 0
        current_run_length = 0
        for bit in block:
            if bit == '1':
                current_run_length += 1
                max_run_length = max(max_run_length, current_run_length)
            else:
                current_run_length = 0
        if max_run_length <= 1:
            V[0] += 1
        elif max_run_length == 2:
            V[1] += 1
        elif max_run_length == 3:
            V[2] += 1
        else:
            V[3] += 1
    Pi = [0.2148, 0.3672, 0.2305, 0.1875]
    X_squared = sum(((V[i] - 16 * Pi[i]) ** 2) / (16 * Pi[i]) for i in range(4))
    P_value = math.erfc(X_squared / 2)
    return P_value


