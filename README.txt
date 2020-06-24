# A small but gluttonous script in Python3 for generating the reference genome with structural variations introduced into it.

## Use
genome_generator.py [-h] [--genome GENOME] [--bed BED]
                         [--output_base_name OUTPUT_BASE_NAME]

## Script require
1. Unzipped reference genome file
2. Sorted bed file with a list of variations. File format

CHROM	start	end	type	seq	strand

The names of the chromosomes must match in the reference genome and in the bed file. If there is no chromosome in the bed file, it is assumed that there are no variations in it and it will be written to the new file unchanged. If the names of the chromosomes do not match, respectively, all chromosomes will be rewritten unchanged.
The script can work with the following structural variations
- deletions
- insertions
- inversions (the reverse complementary sequence will be written)
- duplications
3. Optional - name for the output file

## The output script gives is the file with a new reference genome, but the sequence of each chromosome is represented by one line. To get a standard FASTA file with a string length of 60 characters, please use the seqkit toolkit

seqkit seq -w 60 artificial_genome.fa> narrow_genome.fa

## System requirements:
1. python3
2. biopython (v1.17)
3.seqkit (https://github.com/shenwei356/seqkit)

RAM requirements - to work with human genome the 32 GB, 8 GB is enough for the yeast genome

## Test data
Test files are attached to this script - test_bed.bed and test_genome.fasta. When you run the script with these files, the atrificial_genome.fa file is generated. Intervals and the genome are written in a special way so that the result of the program can be easily seen - insertions are the word (ВСТАВКА), and ДЕЛЕЦИЯ will disappear from the genome. ДУПЛИКАЦИЯ, respectively, doubles. In chromosome 4, you can see the inversion.
