import argparse
import json
import os
import multiprocessing as mp

from functions import number_selection, graph


def main(config_path, operation):
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    match operation:
        case "number_search":
            number_selection(config["card_json"], config["hash_value"], config["last_four"], config["bin"], mp.cpu_count())
        case "graph":
            graph(config["card_json"], config["hash_value"], config["last_four"], config["bin"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some cryptographic operations.")
    parser.add_argument("--config_path", type=str, default=os.path.join('lab_4', 'config.json'), help="Path to the JSON configuration file.")
    parser.add_argument("--operation", type=str, default="number_search", help="Operation to perform (number_search or graph).")
    args = parser.parse_args()
    main(args.config_path, args.operation)