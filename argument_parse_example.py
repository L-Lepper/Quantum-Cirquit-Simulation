#!/usr/bin/env python3 
#allows to start direktly from comand line or dubble click

#example and tutorial: https://realpython.com/command-line-interfaces-python-argparse/
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
    my_parser.add_argument('--Path','-p',
                       metavar='path',
                       type=str,
                       help='the path to list')
    
    my_parser.add_argument('--Path2','-p2',
                       metavar='path',
                       type=str,
                       help='the path to list')
    

    my_parser.add_argument('--verbose','-v',
                       help='activate  verbose mode')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    input_path = args.Path

    if not os.path.isdir(input_path):
        print('The path specified does not exist')
        sys.exit()

    args = my_parser.parse_args()


    print('\n'.join(os.listdir(input_path)))
