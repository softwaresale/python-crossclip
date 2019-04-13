
import sys
import argparse
from crossclip.clipboard import Clipboard

parser = argparse.ArgumentParser(prog='crossclip', description='A commandline script based off of the python module crossclip')

parser.add_argument('-c', '--copy', action='store_true', default=False, description='Copy text to the clipboard')
parser.add_argument('-p', '--paste', action='store_true', default=False, description='Paste text from the clipboard')
parser.add_argument('text', description='Text to be copied to the clipboard')

def main(args_list=None):

    cb = Clipboard()

    # Set up arguments
    if args_list is None:
        args_list = sys.arg

    # Parse command line arguments
    args = parser.parse_args(args_list)

    # Determine what to do
    if args.copy:
        cb.set_text(args.text)
    elif args.paste:
        text = cb.get_text()
        print(text)
    else:
        return 1

    return 0
