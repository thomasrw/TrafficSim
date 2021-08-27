#!/bin/sh

#SBATCH -n 1    #tasks requested
#SBATCH -c 1 	#cores requested per task	
#SBATCH --array=0-99

module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo

TEST_NUM=$SLURM_ARRAY_TASK_ID

i="0"
while [ $i -lt 10 ]
do
/home/thoma525/helloTraci_5.py CAV100_5_$TEST_NUM CAV100_$TEST_NUM --nogui &
TEST_NUM=$((TEST_NUM + 100))
i=$((i + 1))
done
wait

echo success $SLURM_ARRAY_TASK_ID

