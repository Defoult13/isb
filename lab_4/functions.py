import json
import logging
import matplotlib.pyplot as plt
import multiprocessing as mp
import time
import hashlib


logging.basicConfig(level=logging.INFO)


def number_check(hash_str: str, last_numbers: str, bins: list, mid_num: int) -> str:
    """
    Checks the card number with the specified number to match the hash.

    param:
    hash_str (str): A hash string for comparing hashes of card numbers.
    last_numbers (str): The last digits of the card number.
    bins (list): A list of bins for generating card numbers.
    mid_num (int): The number to generate the card number.
    
    return:
    str: The card number corresponding to the hash, if found, else None.
    """
    for bin in bins:
        card_number = f"{bin}{mid_num:06d}{last_numbers}"
        if hashlib.sha224(card_number.encode()).hexdigest() == hash_str:
            return card_number
    return None


def number_selection(save_path: str, hash_str: str, last_numbers: str, bins: list, process_count: int) -> None:
    """
    Search for credit card numbers, by hash, and save them to a file.
    The function uses multiple processes to reduce the search time.

    param:
    save_path (str): The path to save the file.
    hash_str (str): A hash string for hashes of card numbers.
    last_numbers (str): The last digits of the card number.
    bins (list): A list of bins for generating card numbers.
    """
    found_numbers = list()
    with mp.Pool(processes=process_count) as p:
        results = p.starmap(number_check, [(hash_str, last_numbers, bins, i) for i in range(0, 999999)])
        for result in results:
            if result is not None:
                found_numbers.append(result)
    try:
        with open(save_path, "w", encoding="utf-8") as fp:
            json.dump({"card_numbers": found_numbers}, fp)
    except Exception as ex:
        logging.error(f"Failed to save dictionary: {ex}\n")


def luna(card_number: str) -> bool:
    """
    Checking the credit card number using the Moon algorithm.

    param:
    card_number (str): The credit card number.
    
    return:
    bool: The result of the check
    """
    check = int(card_number[-1])
    card_number = [int(i) for i in card_number]
    for i in range(1, len(card_number), 2):
        card_number[i] *= 2
        if card_number[i] > 9:
            card_number[i] = (card_number[i] // 10) + (card_number[i] % 10)
    total_sum = sum(card_number)
    check_sum = (10 - (total_sum % 10)) % 10
    return check_sum == check


def graph(save_path: str, hash_str: str, last_numbers: str, bins: list) -> None:
    """
    Generate a graph showing the dependency of time on the number of processes.

    param:
    save_path (str): The path to save the graph image.
    hash_str (str): A hash string for hashes of card numbers.
    last_numbers (str): The last digits of the card number.
    bins (list): A list of bins for generating card numbers.
    max_processes (int): The maximum number of processes to use for the graph.
    """
    process_range = range(1, int(mp.cpu_count()*1.5) + 1)
    times = []
    for processes in process_range:
        start = time.time()
        number_selection(save_path, hash_str, last_numbers, bins, processes)
        end = time.time() - start
        times.append(end)
        print(f"Processes: {processes}, Time taken: {end} seconds")
    
    plt.plot(process_range, times)
    plt.xlabel('Number of Processes')
    plt.ylabel('Time (seconds)')
    plt.title('Dependency of Time on Number of Processes')
    plt.grid(True)
    plt.savefig(save_path)
    plt.show()