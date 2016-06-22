from __future__ import print_function
import sys
import json
import background
import blob_tracker

usage_str = "Usage: stampede-tools <command> <params_file>"

def main():

    if len(sys.argv) != 3:
        print()
        print("Error: too few arguments")
        print()
        print(usage_str)
        print()
        sys.exit(0)
    
    command = sys.argv[1]
    params_file = sys.argv[2]
    
    with open(params_file,'r') as f:
        params = json.load(f)
    
    if command == 'background':
        background.median_background(params)
    elif command == 'tracking':
        blob_tracker.track_blobs(params)
    else:
        print()
        print("Error: unknown command")
        print()
        print(usage_str)
        print()
        print("allowed commands = background, tracking")
        print()


# -------------------------------------------------------------------------
if __name__ == '__main__':

    main()

