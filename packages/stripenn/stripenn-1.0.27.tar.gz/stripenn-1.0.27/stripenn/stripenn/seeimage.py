import argparse
import cooler
import multiprocessing
from stripenn import getStripe
import os
import shutil
import errno
import pandas as pd
import numpy as np
import warnings
import time
import sys

def argumentParser():
    parser = argparse.ArgumentParser(description='Stripenn')
    parser.add_argument("cool", help="Balanced cool file.")
    parser.add_argument('out', help="Path to output directory.")
    parser.add_argument('--norm', help="Normalization method. It should be one of the column name of Cooler.bin(). Check it with Cooler.bins().columns (e.g., KR, VC, VC_SQRT)", default='KR')
    parser.add_argument("-k", '--chrom', help="Set of chromosomes. e.g., 'chr1,chr2,chr3', 'all' will generate stripes from all chromosomes", default='all')
    parser.add_argument("-c","--canny", help="Canny edge detection parameter.", default=2.5)
    parser.add_argument('-l','--minL', help="Minimum length of stripe.",default=10)
    parser.add_argument('-w','--maxW', help="Maximum width of stripe.",default=8)
    parser.add_argument('-m','--maxpixel', help="Percentiles of the contact frequency data to saturate the image. Separated by comma. Default = 0.95,0.96,0.97,0.98,0.99", default='0.95,0.96,0.97,0.98,0.99')
    num_cores = multiprocessing.cpu_count()
    parser.add_argument('-n','--numcores', help='The number of cores will be used.', default = num_cores)
    parser.add_argument('-p', '--pvalue', help='P-value cutoff for stripe.', default = 0.2)
    args = parser.parse_args()

    cool = args.cool
    out = args.out
    if out[-1] != '/':
        out += '/'
    norm = args.norm
    chroms = args.chrom
    chroms = chroms.split(',')
    canny = float(args.canny)
    minH = int(args.minL)
    maxW = int(args.maxW)
    maxpixel = args.maxpixel
    maxpixel = maxpixel.split(',')
    maxpixel = list(map(float, maxpixel))
    core = int(args.numcores)
    pcut = float(args.pvalue)

    return(cool, out, norm, chroms, canny, minH, maxW, maxpixel, core, pcut)


def seeimage():
    print('seeimage_asdf')
    return 0


