#!/bin/sh

#SBATCH -n 1000    #tasks requested
#SBATCH -c 1 	#cores requested per task	

module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo


srun --multi-prog demand.conf
