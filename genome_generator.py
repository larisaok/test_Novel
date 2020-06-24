#!/bin/python3

import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description='This script will help you with generating the fasta genome file '
                                             'based on reference fasta and bed file with variations')

# Argument parsing
parser.add_argument('--genome', '-g',
                    help='Specify the genome fasta file')
parser.add_argument('--bed', '-b',
                    help='Specify the .bed file with genomic variations')
parser.add_argument('--output_base_name', '-o',
                    default='artificial_genome',
                    type=str,
                    help='Specify the prefix for output files')

args = parser.parse_args()
genome = args.genome
bed = args.bed
output_base_name = args.output_base_name

# Reading the contents of a bed file in a python dictionary.
# The key is the name of the chromosome, the value is a list of lists with variations.
# In each interval, the start of variation ([0]), the end of variation ([1]),
# type of variation ([2]), nucleotides ([3]) are recorded.

with open(bed, 'r') as bed_file:
    bed = {}
    for line in bed_file:
        interval = line.strip().split()
        if interval[0] in bed:
            bed[interval[0]].append(interval[1:6])
        else:
            bed[interval[0]] = []
            bed[interval[0]].append(interval[1:6])

# Creating the index for fasta file
fasta = SeqIO.index(genome, "fasta")


def inversion(sequence):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N',
                  'a': 't', 'c': 'g', 'g': 'c', 't': 'a'}
    return ''.join([complement[base] for base in sequence[::-1]])


with open(output_base_name + '.fa', 'w') as out:
    for chromosome in fasta:
        out.write('>' + chromosome + '\n')
        end_left = 0
        start_right = 0
        end_right = 0
        try:
            for interval in bed[chromosome]:
                start_right = int(interval[0])  # take an interval (let's call it the right interval)
                # and write its coordinates to variables
                end_right = int(interval[1])
                out.write(str(fasta[chromosome].seq[end_left:start_right]))  # take the unchanged chromosome between
                # the current (right) interval and the left (previous) interval.
                # At the first iteration, the end of the left interval is the beginning of the chromosome.
                if interval[2] == 'del':  # interval[2] element of list contains information about variation types
                    end_left = int(interval[1])
                    continue  # if the type of interval is a deletion,
                    # write its end to end_left and go to the next interval
                if interval[2] == 'ins':
                    out.write(interval[3])  # if the interval type is insertion,
                    # take a sequence from the corresponding column and paste it into the file
                if interval[2] == 'inv':
                    out.write(inversion(fasta[chromosome].seq[start_right:end_right]))
                if interval[2] == 'dup':
                    out.write(str(fasta[chromosome].seq[start_right:end_right]))
                    out.write(str(fasta[chromosome].seq[start_right:end_right]))
                end_left = int(interval[1])
            out.write(str(fasta[chromosome].seq[end_right:]) + '\n')  # write the end of chromosome to the file
        except KeyError:  # in the absence of variations in some chromosome, we write its sequence to a file
            out.write(str(fasta[chromosome].seq) + '\n')
            continue
