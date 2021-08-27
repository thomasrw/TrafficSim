#!/bin/sh

#SBATCH -n 1    #tasks requested
#SBATCH -c 1 	#cores requested per task	


module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo



/home/thoma525/helloTraci.py CAV100_1 CAV100_1 --nogui

echo success $SLURM_ARRAY_TASK_ID

