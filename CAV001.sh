#!/bin/sh

#SBATCH -n 1    #tasks requested
#SBATCH -c 10 	#cores requested per task	
#SBATCH --array=0-99

module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo

#run CAV001 100-199 for pln_size 1-10, with 1 being no limit (anything < 2 not enforced)
TEST_NUM=$((SLURM_ARRAY_TASK_ID + 100))

i="1"
while [ $i -lt 11 ]
do
/home/thoma525/helloTraci.py CAV001_$TEST_NUM CAV001_$TEST_NUM $i --nogui &
#TEST_NUM=$((TEST_NUM + 100))
i=$((i + 1))
done
wait

echo success $SLURM_ARRAY_TASK_ID

