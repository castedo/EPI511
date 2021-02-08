import numpy as np
import pandas as pd
from pathlib import Path

def index_past(lst, value):
    '''index past the last element equal to `value`'''
    return len(lst) - list(reversed(lst)).index(value)

class MiniHapMap:

    def __init__(self, data_dir, num_chromosomes=22):
        '''Initialize for data directory at location set in `data_dir` parameter'''
        self.data_dir = Path(data_dir)

        # read snp file into a pandas dataframe
        self.snps = pd.read_table(
            self.data_dir / 'HapMap3.snp',
            sep='\s+', # columns are separated by whitespace
            # names of the columns
            names=[None, 'chromosome', 'morgans', 'position', 'ref', 'alt'],
            index_col=0
        )
        self.snps = self.snps[self.snps.chromosome <= num_chromosomes]

        # initialize zero rows of individual and genotype data
        self.individuals = pd.DataFrame(columns=['sex', 'population'])
        self.genotypes = np.ma.empty((len(self.snps), 0), dtype=np.int8)

    def load_population(self, population):
        '''Read file of population data and load into memory'''

        # read in individual data
        ind = pd.read_table(
            self.data_dir / (population+ '.ind'),
            sep='\s+',
            names=[None, 'sex', 'population'],
            index_col=0
        )
        self.individuals = self.individuals.append(ind)

        # read in genotype data
        raw = np.full((len(self.snps), len(ind)), -128, dtype=np.int8)
        r = 0
        with open(self.data_dir / (population + '.geno'), mode='rb') as file:
            for line in file:
                if r < len(raw):
                    # ASCII byte '0' is encoded as the number 48
                    raw[r] = np.frombuffer(line.rstrip(), dtype=np.int8) - 48
                    r += 1
        raw = np.ma.masked_outside(raw, 0, 2)
        self.genotypes = np.ma.append(self.genotypes, raw, axis=1)

    def geno_pop(self, population, chromosome=None):
        pop_begin = list(self.individuals.population).index(population)
        pop_end = index_past(self.individuals.population, population)
        ret = self.genotypes[:, pop_begin:pop_end]
        if chromosome is not None:
            ret = ret[self.snps.chromosome == chromosome, :]
        return ret
