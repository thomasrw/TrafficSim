#!/bin/sh

#SBATCH --array=1-100
##SBATCH -N 1     #nodes requested
#SBATCH -n 1     #tasks requested changed to number of cores needed per Nathan Elger guidance
##SBATCH -c 10    #cpus per task commented out per Nathan Elger guidance	
#SBATCH --output=/dev/null  #suppress standard output
#SBATCH --error=/dev/null   #suppress standard error

##todo run demand_formatter.py on CAV [arg1] _ [arg2] to ensure catchup properly defined
##todo CAV [array task] for inputs 100-199 for sizes x
#todo Gather metrics for CAV [array task] for inputs 100-199
#todo remove all logfiles generated leaving only metrics.csv files for CAV [array task]_size

module load sumo
module load python3/anaconda/2019.03

export SUMO_HOME=/work/apps/sumo/share/sumo

#run CAV008 100-199 for pln_size 1-10, with 1 being no limit (anything < 1 not enforced)
#TEST_NUM=$((SLURM_ARRAY_TASK_ID + 99))

SIZE="6"
PERCENT=$(printf "%03d" $SLURM_ARRAY_TASK_ID)

#cleans CAV$PERCENT for test_num's 100-199 one at a time (shouldn't take long)
i="100"
while [ $i -lt 101 ]
do
python3 /work/thoma525/demand_formatter.py $PERCENT $i
i=$((i + 1))
done

#run CAV$PERCENT for test_num's 100-199, ten at a time
j="101"
while [ $j -lt 102 ]
do
i="0"
while [ $i -lt 1 ]
do
/work/thoma525/helloTraci_log.py single6CAV$PERCENT"_${j}""_${SIZE}" CAV$PERCENT"_${j}" $SIZE --nogui &
j=$((j + 1))
i=$((i + 1))
done
wait
done

#collect metrics for all CAV$PERCENT runs (100-199), ten at a time
j="101"
k="100"
while [ $j -lt 102 ]
do
i="0"
while [ $i -lt 1 ]
do
python3 /work/thoma525/eval_3.py single6CAV$PERCENT $j singleCAV$PERCENT"_size_${SIZE}" $SIZE &
j=$((j + 1))
i=$((i + 1))
done
wait
#clean up after each run of 10
while [ $k -lt $j ]
do
#rm /work/thoma525/CAV$PERCENT"_${k}""_${SIZE}""_tripinfo"
#rm /work/thoma525/CAV$PERCENT"_${k}""_${SIZE}""_platoon_status.xml"
#rm /work/thoma525/CAV$PERCENT"_${k}""_${SIZE}""_validation_dets.xml"
k=$((k + 1))
done

done

#final clean up log files from simulation runs, leaving behind only metrics.csv file
#rm /work/thoma525/CAV$PERCENT"_${j}""_${SIZE}""_tripinfo"
#rm /work/thoma525/CAV$PERCENT"_${j}""_${SIZE}""_platoon_status.xml"
#rm /work/thoma525/CAV$PERCENT"_${j}""_${SIZE}""_validation_dets.xml"



echo success $SLURM_ARRAY_TASK_ID


