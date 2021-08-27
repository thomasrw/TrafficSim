#!/bin/sh

#SBATCH -n 1    #tasks requested
#SBATCH -c 1 	#cores requested per task	
#SBATCH --array=800-899

module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo



python3 /home/thoma525/add_connected.py $SLURM_ARRAY_TASK_ID

TEST_NUM=$((SLURM_ARRAY_TASK_ID + 100))

python3 /home/thoma525/add_connected.py $TEST_NUM
