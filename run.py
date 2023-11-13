# run.py

from src import main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the COVID-19 Spread Cellular Automata Model")
    parser.add_argument("--input-path", type=str, required=True , help="Path to input board")
    parser.add_argument("--output-path", type=str, default="./data/output/", help="Path to save resulting board")
    parser.add_argument("--num-steps", type=int, default=100, help="How many stemps to simulate for the model")
    parser.add_argument("--visualize", action="store_true", help="Whether to visualize the data at each step")
    parser.add_argument("--debug", action="store_true", help="Debug flag (for print statements)")
    args = parser.parse_args()
    main.main(args)