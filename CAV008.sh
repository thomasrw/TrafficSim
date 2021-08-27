#!/bin/sh

#SBATCH --array=0-99
##SBATCH -N 1     #nodes requested
#SBATCH -n 1     #tasks requested
#SBATCH -c 10    #cpus per task	


module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo

#run CAV008 100-199 for pln_size 1-10, with 1 being no limit (anything < 2 not enforced)
TEST_NUM=$((SLURM_ARRAY_TASK_ID + 100))

i="1"
while [ $i -lt 11 ]
do
# logname demand_file pltn_size
/home/thoma525/helloTraci.py CAV008_$TEST_NUM"_${i}" CAV008_$TEST_NUM $i --nogui &
#TEST_NUM=$((TEST_NUM + 100))
i=$((i + 1))
done
wait

echo success $SLURM_ARRAY_TASK_ID

