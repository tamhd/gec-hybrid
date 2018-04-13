#!/usr/bin/env python

""" Calculate the percentage of edits made on a dataset
"""

from __future__ import division, print_function
import sys
import argparse
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser()
parser.add_argument("source", type=str, help="source file containing english written by ESL")
parser.add_argument("hypothesis", type=str, help="output of system correcting the source file")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()

if args.verbose:
    logger.info("verbosity turned on")
    logger.warn("A lot of messages will be printed!")


def main():
    """ calculate the number of edit made in the source
    """
    src_count, hyp_count = 0, 0
    edit_count = 0
    with open(args.source, mode="r") as sopen, open(args.hypothesis, mode="r") as hopen:
        for src_tok, hyp_tok in zip(sopen, hopen):
            src_toks, hyp_toks = src_tok.strip().split(), hyp_tok.strip().split()
            src_len, hyp_len = len(src_toks), len(hyp_toks)

            # create a table to calculate the dp matrix
            dp = [[None for _ in range(hyp_len+1)] for _ in range(src_len+1)]

            for idx in range(hyp_len+1):
                dp[0][idx] = idx

            for idx in range(src_len+1):
                dp[idx][0] = idx

            for id1 in range(1, src_len+1):
                for id2 in range(1, hyp_len+1):
                    if src_toks[id1-1] == hyp_toks[id2-1]:
                        dp[id1][id2] = dp[id1-1][id2-1]
                    else:
                        dp[id1][id2] = min(dp[id1-1][id2-1], dp[id1][id2-1], dp[id1-1][id2]) + 1

            src_count += src_len
            hyp_count += hyp_len
            edit_count += dp[src_len][hyp_len]
            

    print("Statistics")
    print("Source Size \t{0}".format(src_count))
    print("Hypothesis Size \t{0}".format(hyp_count))
    print("Edit Count \t{0}".format(edit_count))
    print("Edit Ratio \t{0}".format(edit_count / src_count))


if __name__ == "__main__":
    main()