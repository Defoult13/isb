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

