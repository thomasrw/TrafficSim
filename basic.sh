#!/bin/sh
#SBATCH --job-name=test
#SBATCH --output test%j.out
#SBATCH --error test%j.err
#SBATCH -N 1
#SBATCH -n 7
#SBATCH -p defq
#SBATCH --exclude=node[174-238]

##Load your modules first:

module load R/gcc/3.6.0


##Add your code here:

hostname
date
