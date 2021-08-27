#!/bin/sh

#SBATCH -N 1    #nodes requested
#SBATCH -n 4    #tasks requested
#SBATCH -c 1 	#cores requested per task	

module load sumo

for (( i=0; i < $SLURM_NTASKS; i++ )); do
	python hello.py $i &
done

wait
