import json
import os
import math

def bit_frequency_test(sequence):
    transformed_sequence = [1 if bit == '1' else -1 for bit in sequence]
    Sn = sum(transformed_sequence) / math.sqrt(len(sequence))
    P_value = math.erfc(Sn / math.sqrt(2))
    return P_value

