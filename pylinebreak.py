#!/usr/bin/env python
################################################################################
#   Program:        pylinebreak
#   Author:         James Hendrie   (hendrie dot james at gmail dot com)
#   Version:        0.12
#   License:        GPLv3.  See LICENSE.txt for more details.
#   Date:           2012-02-27
#   Description:    Formats long lines, breaking them into smaller (80-char
#                   maximum) lines for easier reading on a TTY / shell terminal
################################################################################

import sys
import textwrap


def print_help():
    '''
    Prints the help for PyLineBreak
    '''
    help_str = '''
Usage:  pylinebreak [input] [output]
\n
PyLineBreak reads from a file (or stdin), formats any especially long lines
that it finds in the text, and outputs to stdout (or, optionally, a file).

Examples:

pylinebreak FILE.txt
    This will read the text in FILE.txt, format it, and dump it to stdout

pylinebreak FILE_1.txt FILE_2.txt
    This will read the text from FILE_1.txt, format the text, and write it to
    FILE_2.txt.

cat somefile | pylinebreak - | some_other_program
    This concatenates the text from 'somefile', dumping it to stdout.  Stdout is
    then piped to pylinbreak which reads from stdin ('-'), the results of which
    are then piped again to some_other_program.\n
    '''
    print (help_str)

def print_version():
    '''
    Prints the version number, 'credits' and contact info
    '''
    version_str = '''
    \n
    PyLineBreak version 0.12.
    Contact:  James Hendrie (hendrie dot james at gmail dot com)\n
    '''
    print (version_str)

def startup():
    '''
    Sets initial variables, returning a dict with settings
    '''
    ##  Set the margin to 80 characters.  In the future, I may add an option
    ##  to allow this to be changed with an argument
    margin = 80

    ##  Set the 'output mode' to 'file'.  The two valid 'modes' are either
    ##  'file' or 'stdout'.  'file' will write to a file, 'stdout' writes to
    ##  stdout.
    output = 'file'

    ##  Create the settings dict
    settings = {'margin':margin, 'output':output}

    return settings


def format_text(text, settings):
    '''
    Formats the text
    '''

    ##  Get settings from settings dict
    margin = settings['margin']

    ##  Format the string properly with Python's textwrap module
    new_text = textwrap.fill(text, replace_whitespace=False,
            width = margin, drop_whitespace=False)

    return new_text



def parse_args(args, settings):
    '''
    Parse the arguments passed to the program at execution
    '''
    ##  If the command line ends with -h or --help, print the help
    if args[-1] == '-h' or args[-1] == '--help':
        print_help()
        sys.exit()

    ##  If the command line ends with -v or --verison, print the version
    elif args[-1] == '-v' or args[-1] == '--version':
        print_version()
        sys.exit()
    else:
        ##  If the only thing typed was the program name and one other thing
        if len(args) == 2:
            ##  If that other thing was a '-' character (stdin)
            if args[-1] == '-':
                ##  Read all text directly from stdin
                text = sys.stdin.read()
                ##  Set 'output' mode to 'stdout'
                settings['output'] = 'stdout'
                ##  Just set 'output_file' to an empty string
                output_file = ''
            else:
                ##  If it wasn't a '-', we'll assume it was a file.
                try:
                    ##  Try opening the file
                    text_file = open(args[-1])
                except IOError:
                    print ("Error:  Can't open %s for reading." % args[-2])
                    sys.exit()

                text = text_file.read()
                text_file.close()

            ##  Since no output file was specified, dump output to stdout
            settings['output'] = 'stdout'
            output_file = ''

        ##  If the user typed the program name and two other things
        elif len(args) == 3:
            output_file = args[-1]
            try:
                text_file = open(args[-2], 'r')
            except IOError:
                print ("Error:  Can't open %s for reading." % args[-2])
                sys.exit()

            ##  Read text from the file
            text = text_file.read()
            text_file.close()

            ##  Set output mode to 'file', to indicate that a file will be
            ##  be written to disk later on
            settings['output'] = 'file'

        ##  If they typed a bunch of crap
        else:
            print ("Error:  Too many arguments.")
            sys.exit()

    return settings, text, output_file


def main():
    ##  Get initial settings
    settings = startup()
    ##  Update settings, get text, get the output file (if any)
    settings, text, output_file = parse_args(sys.argv, settings)
    ##  Format the text
    text = format_text(text, settings)
    ##  If no output file was specified
    if settings['output'] == 'stdout':
        ##  Just dump everything to stdout
        print (text)
        sys.exit()
    ##  If an output file was specified
    elif settings['output'] == 'file':
        try:
            text_file = open(output_file, 'w')
        except IOError:
            print ("ERROR:  Can't write to %s" % output_file)
            sys.exit()
        
        for line in text:
            text_file.write(line)
        text_file.close()


if __name__ == '__main__':
    main()
