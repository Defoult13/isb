import json
import os
import math

from typing import List


def bit_frequency_test(sequence: str) -> float:
    """
    Calculate the P-value of the Bit Frequency Test for a given binary sequence.

    Args:
        sequence (str): The binary sequence.

    Returns:
        float: The P-value of the Bit Frequency Test.
    """
    transformed_sequence = [1 if bit == '1' else -1 for bit in sequence]
    Sn = sum(transformed_sequence) / math.sqrt(len(sequence))
    P_value = math.erfc(Sn / math.sqrt(2))
    return P_value


def consecutive_bit_test(sequence: str) -> float:
    """
    Calculate the P-value of the Consecutive Bit Test for a given binary sequence.

    Args:
        sequence (str): The binary sequence.

    Returns:
        float: The P-value of the Consecutive Bit Test.
    """
    n = len(sequence)
    y = sum(int(bit) for bit in sequence) / n
    if abs(y - 1/2) >= 2 / math.sqrt(n):
        return 0
    Vn = sum(1 for i in range(n - 1) if sequence[i] != sequence[i + 1])
    P_value = math.erfc(abs(Vn - 2 * n * y * (1 - y)) / (2 * math.sqrt(2 * n) * y * (1 - y)))
    return P_value


def longest_run_of_ones_test(sequence: str, block_size: int = 8) -> float:
    """
    Calculate the P-value of the Longest Run of Ones Test for a given binary sequence.

    Args:
        sequence (str): The binary sequence.
        block_size (int, optional): The size of blocks to divide the sequence into. Defaults to 8.

    Returns:
        float: The P-value of the Longest Run of Ones Test.
    """
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


def main() -> None:
    """
    Main function to read input, perform tests, and write results to an output file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
    path_input = config_data["input"]
    path_output = config_data["output"]
    
    input_dir = os.path.dirname(path_input)
    gen_results_path = os.path.join(input_dir, 'gen_results.json')
    
    with open(gen_results_path, 'r') as results_file:
        results_data = json.load(results_file)
    
    with open(path_output, 'w') as output_file:
        for generator, sequence in results_data.items():
            output_file.write(f"Generator: {generator}\n")
            output_file.write("Bit Frequency Test P-value: {}\n".format(bit_frequency_test(sequence)))
            output_file.write("Consecutive Bit Test P-value: {}\n".format(consecutive_bit_test(sequence)))
            output_file.write("Longest Run of Ones Test P-value: {}\n".format(longest_run_of_ones_test(sequence)))
            output_file.write("\n")


if __name__ == "__main__":
    main()
