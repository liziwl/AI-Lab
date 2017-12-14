import argparse


def ise_parse_command_line():
    parser = argparse.ArgumentParser(description="ISE -- Influence Spread Estimator")
    parser.add_argument("-i", metavar="<social network>", dest="network", type=str, required=True,
                        help="the absolute path of the social network file.")

    parser.add_argument("-s", metavar="<seed set>", dest="seed", type=str, required=True,
                        help="the absolute path of the seed set file.")

    parser.add_argument("-m", metavar="<diffusion model>", dest="model", type=str, required=True,
                        help="diffusion model which can only be IC or LT.")

    parser.add_argument("-b", metavar="<termination type>", dest="termination", type=int, required=True,
                        help="specifies the termination manner and the value can\
                        only be 0 or 1. If it is set to 0, the termination condition is as the same\
                        defined in your algorithm. Otherwise, the maximal time budget specifies\
                        the termination condition of your algorithm.")

    parser.add_argument("-t", metavar="<time budget>", dest="utime", type=int, required=True,
                        help="a positive number which indicates how many seconds\
                        (in Wall clock time, range: [60s, 1200s]) your algorithm can spend on\
                        this instance. If the <termination type> is 0, it still needs to accept -t\
                        <time budget>, but can just ignore it while estimating.")

    parser.add_argument("-r", metavar="<random seed>", dest="rand", type=str, default=None,
                        help="random seed used in the algorithm")
    args = parser.parse_args()
    # print args.network, args.seed, args.model, args.termination, args.utime, args.rand
    if args.termination != 0 and args.termination != 1:
        parser.error('argument -b: should be 0 or 1.')
    return args.network, args.seed, args.model, args.termination, args.utime, args.rand


def imp_parse_command_line():
    parser = argparse.ArgumentParser(description="IMP -- Influence Maximization Processor")
    parser.add_argument("-i", metavar="<social network>", dest="network", type=str, required=True,
                        help="the absolute path of the social network file.")

    parser.add_argument("-k", metavar="<predefined size of the seed set>", dest="size", type=int, required=True,
                        help="a positive integer.")

    parser.add_argument("-m", metavar="<diffusion model>", dest="model", type=str, required=True,
                        help="diffusion model which can only be IC or LT.")

    parser.add_argument("-b", metavar="<termination type>", dest="termination", type=int, required=True,
                        help="specifies the termination manner and the value can\
                            only be 0 or 1. If it is set to 0, the termination condition is as the same\
                            defined in your algorithm. Otherwise, the maximal time budget specifies\
                            the termination condition of your algorithm.")

    parser.add_argument("-t", metavar="<time budget>", dest="utime", type=int, required=True,
                        help="a positive number which indicates how many seconds\
                            (in Wall clock time, range: [60s, 1200s]) your algorithm can spend on\
                            this instance. If the <termination type> is 0, it still needs to accept -t\
                            <time budget>, but can just ignore it while estimating.")

    parser.add_argument("-r", metavar="<random seed>", dest="rand", type=str, default=None,
                        help="random seed used in the algorithm")
    args = parser.parse_args()
    # print args.network, args.size, args.model, args.termination, args.utime, args.rand
    if args.termination != 0 and args.termination != 1:
        parser.error('argument -b: should be 0 or 1.')
    return args.network, args.size, args.model, args.termination, args.utime, args.rand


if __name__ == "__main__":
    pass
    # imp_parse_command_line()
    # ise_parse_command_line()
