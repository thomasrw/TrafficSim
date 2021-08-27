#!/bin/sh

##SBATCH -N 2    #nodes requested
#SBATCH -n 1000    #tasks requested
#SBATCH -c 1 	#cores requested per task	

module load sumo
module load python3/anaconda/2019.03

srun --multi-prog silly.conf
