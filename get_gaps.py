#!/usr/bin/env python


from argparse import ArgumentParser
from Bio import SeqIO

def get_Ns(seq, chrname):
    all_pos = [pos for pos, char in enumerate(seq) if char == 'N' or char == 'n']
    res = []
    current = []
    for e in all_pos:
        if not current:
            current.append(e)
        else:
            if e - current[-1] == 1:
                current.append(e)
            else:
                print '\t'.join(map(str,[chrname,current[0],current[-1]]))
                current = [e]

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('ref')
    args = parser.parse_args()
    fasta_sequences = SeqIO.parse(open(args.ref),'fasta')
    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        get_Ns(sequence, name)
