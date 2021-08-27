#!/bin/sh

#SBATCH -n 1    #tasks requested
#SBATCH -c 25 	#cores requested per task	
#SBATCH --array=0-39

module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo

#TEST_NUM=$SLURM_ARRAY_TASK_ID
TEST_NUM=$((SLURM_ARRAY_TASK_ID * 25))

i="0"
while [ $i -lt 25 ]
do
#/home/thoma525/helloTraci.py CAV025_$TEST_NUM CAV025_$TEST_NUM --nogui &
python3 /home/thoma525/tripEval.py CAV100 $TEST_NUM &
TEST_NUM=$((TEST_NUM + 1))
i=$((i + 1))
done
wait

echo success $SLURM_ARRAY_TASK_ID

