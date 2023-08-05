"""Console script for quickzoom."""
import argparse
import sys
from quickzoom import connect

def main():
    """Console script for quickzoom."""
    parser = argparse.ArgumentParser()
    parser.add_argument('roomlabel',  nargs="?", default=None, help="Quickzoom will search for that label in your config. If the label exists, it will read the meeting id and password saved for that label and connect to it via zoom.")
    parser.add_argument("-n", "--newroom", help="Create a new room in your config. You will be prompted for a room label, zoom meeting id and zoom password.", action='store_true')
    args = parser.parse_args()

    print("Arguments: " + str(args))

    connect.run(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
