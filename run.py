# run.py

from src import main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the COVID-19 Spread Cellular Automata Model")
    parser.add_argument("--input-path", type=str, required=True , help="Path to input board")
    parser.add_argument("--output-path", type=str, default="./data/output/", help="Path to save video to")
    parser.add_argument("--num-steps", type=int, default=10, help="How many steps to simulate for the model")
    parser.add_argument("--record", action="store_true", help="Record the cellular automata model")
    parser.add_argument("--video-length", type=int, default=10, help="How long the resulting video should be. Note, if there are less than 10 steps, the video is defaulted to one step a second")
    parser.add_argument("--debug", action="store_true", help="Debug flag (for print statements)")
    args = parser.parse_args()

    if args.record and not args.output_path:
        parser.error("--output-path is required when --record is set.")

    main.main(args)