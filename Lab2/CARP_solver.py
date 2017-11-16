# encoding: utf-8

import sys
import getopt
import os
import re


def main(argv):
    try:
        if len(argv) != 5:
            raise getopt.GetoptError("The argument count should be 5, and now is {}.".format(len(argv)))

        file_name = argv[0]
        if not os.path.isfile(file_name):
            raise IOError("The carp instance file does not exist.")

        termination = ''
        seed = ''
        opts, args = getopt.getopt(argv[1:], "t:s:")
        for opt, arg in opts:
            if opt == '-t':
                termination = int(arg)
            elif opt == '-s':
                pattern = '^[0-9]+$'
                match = re.findall(pattern, arg)
                if len(match) != 0:
                    seed = long(arg)
                else:
                    seed = arg

        print file_name
        print 'termination: ', termination
        print 'seed: ', seed

    except getopt.GetoptError as err:
        print str(err)
        print 'The argument should be <carp instance file> -t <termination> -s <random seed>'
        sys.exit(2)
    except ValueError as err:
        print("Termination argument should be an integer.")
        print 'The argument should be <carp instance file> -t <termination> -s <random seed>'
        sys.exit(2)
    except IOError as err:
        print str(err)
        print 'The argument should be <carp instance file> -t <termination> -s <random seed>'
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
