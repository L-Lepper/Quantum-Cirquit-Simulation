#!/usr/bin/env python3 
#allows to start direktly from comand line or dubble click

#example and tutorial: https://docs.python.org/3/howto/argparse.html
#example and tutorial: https://realpython.com/command-line-interfaces-python-argparse/



# myls.py
# Import the argparse library
import argparse

import os
import sys

if __name__ == '__main__':
    # Create the parser
    my_parser = argparse.ArgumentParser(description='List the content of a folder')

    # Add the arguments
    my_parser.add_argument('--path', '-p',
                       metavar='path_to_list',
                       type=str,
                       help='the path to list')
    
    my_parser.add_argument('--Path2', '-p2',
                       metavar='path',
                       type=str,
                       help='the path to list')

    my_parser.add_argument('--verbose', '-v',
                       metavar='verbose_level',
                       help='set verbose level')
    my_parser.add_argument('--loop', '-l',
                       help='activate loop mode')

    # Execute the parse_args() method
    args = my_parser.parse_args()


# handle all saved arguments: and do stuff :-)
    if args.path:
        input_path = args.path
        if not os.path.isdir(input_path):
            print('The path specified does not exist')
            sys.exit()
        print('\n'.join(os.listdir(input_path)))

    if args.verbose:
        print('Verbose level was set to', args.verbose)
        # could also be a function call

    if args.loop:
        print('loop mode is on')
    else:
        print('loop mode is off')

