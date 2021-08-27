#!/bin/sh

#SBATCH -n 1    #tasks requested
#SBATCH -c 1 	#cores requested per task	
#SBATCH --array=0-98

module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo

TEST_NUM=$SLURM_ARRAY_TASK_ID

TEST_NUM=$((TEST_NUM + 2))
PERCENT=$(printf "%03d" $TEST_NUM)

#i="0"
#while [ $i -lt 10 ]
#do


/home/thoma525/helloTraci.py CAV100_2_$TEST_NUM CAV100_2 $TEST_NUM --nogui


#TEST_NUM=$((TEST_NUM + 100))
#i=$((i + 1))
#done
#wait

echo success $SLURM_ARRAY_TASK_ID

