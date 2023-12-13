# cbm-cellular-automata

run 'python run.py --help' in command line


This repo is organized more like a library as opposed to one dedicated just to create our final model.


## Models
- BasicCellularAutomata
- BasicProbabilisticCellularAutomata
- SEIQRD1ProbabilisticCellularAutomata
- SEIQRD_DevicePCA




# Run Options
- `--input-path` path to input cellular automata grid (`data/input/...`)
- `--device-input-path` path to input device grid (`data/input/...`)
- `--output-path` path to where to save the ouput video (if `--record` flag is set)
- `--device-param1` Float value (0, 1] for device parameter 1
- `--device-param2` Integer value [0, quarantine_delay) for device parameter 2
- `--num-steps` Number of steps to run the cellular automata for
- `--record` set this flag if you want to record a video
- `--video-length` how long do you want the video to be
- `--debug` set this flag for debug logging (**YOU WANT THIS**)

Example run:
`python run.py --input-path=./data/input/SEIQRD2.1.txt --device-input-path=./data/input/SEIQRD_D1.1.txt --output-path=./data/output/SEIQRD11.mp4 --device-param1=0.5 --device-param2=2 --num-steps=50 --record --video-length=20`

