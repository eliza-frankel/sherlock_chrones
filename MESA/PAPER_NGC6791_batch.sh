#!/bin/bash

#SBATCH --account=gr-isochronebldg
#SBATCH --time=70:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --mail-type=END
#SBATCH --mail-user=efrankel@uwyo.edu

# # This is the file that loops through and runs every track!

####################################################################################################
########## THE FOLLOWING IS A CODE TO CHECK CLUSTER RESOURCES WHILE LAUNCHING LARGE GRIDS ##########
####################################### WRITTEN BY ILY RUBIO #######################################
####################################################################################################

# Cluster and resource parameters
USER="efrankel"         # <-- your HPC username
CORE_LIMIT=4794        # 33% of total cluster cores
WAIT_TIME=300          # seconds between usage checks
CORES_PER_JOB=8       # each job requests X cores

# throttling
throttling_threshold=100          # number of jobs before pausing
count=0

CORES_PER_THROTTLING=$((throttling_threshold * CORES_PER_JOB))

#----------------------------
# FUNCTIONS
#----------------------------

check_core_usage() {
    read RUNNING_CORES PENDING_CORES <<< $(arccjobs | awk -v user="$USER" '$1 == user {print $3, $6}')
    RUNNING_CORES=${RUNNING_CORES:-0}
    PENDING_CORES=${PENDING_CORES:-0}
    TOTAL=$((RUNNING_CORES + PENDING_CORES))
    echo "$TOTAL"
}

wait_for_slot() {
    while true; do
        TOTAL_CORES=$(check_core_usage)
        echo "[$(date)] $USER using ${TOTAL_CORES}/${CORE_LIMIT} cores..."

        if (( TOTAL_CORES + CORES_PER_THROTTLING < CORE_LIMIT )); then
            echo "Under limit — proceeding with submission."
            break
        else
            echo "Over limit; waiting $WAIT_TIME seconds..."
            sleep "$WAIT_TIME"
        fi
    done
}


####################################################################################################

source ~/.bashrc
mesa

# Parameters
# 8.3 Gyr
START_MASS=0.80
STOP_MASS=1.17
STEP_MASS=0.01



CONDITIONAL_MASS_ONE=1.11
CONDITIONAL_MASS_TWO=1.148
CONDITIONAL_MASS_THREE=1.153
# CONDITIONAL_MASS_FOUR=1.1588
# CONDITIONAL_MASS_FIVE=1.12969

INITIAL_Z=0.034507 # [Fe/H] = 0.31, [alpha/Fe] = 0.06
INITIAL_Y=0.296310 # dY/dZ = 1.4 - Brogaard et al. 2012

m=$START_MASS
z=$INITIAL_Z
y=$INITIAL_Y


while (( $(echo "$m <= $STOP_MASS" | bc -l) ))
do
	
	if (( count >= throttling_threshold )); then
        echo ">>> Reached throttling threshold: $count jobs."

        #Minor delay between batches
        sleep 10

        #Check core usage
        wait_for_slot

        #Reset batch count
        count=0
    fi



	# # # # EAF - changing the step mass to be denser at higher masses
	# # 0.8 - 1.11; step 0.01 - 31 tracks

	# 1.11 - 1.148; step 0.001 - 38 tracks
	if (( $(echo "$m >= $CONDITIONAL_MASS_ONE" | bc -l) ))  
		then
		STEP_MASS=0.001
	fi

	# 1.148 - 1.153; step 0.0001 - 50 tracks
	if (( $(echo "$m >= $CONDITIONAL_MASS_TWO" | bc -l) ))
		then
		STEP_MASS=0.0001
	fi

	# 1.153 - 1.17; step 0.00005 - 340 tracks
	if (( $(echo "$m >= $CONDITIONAL_MASS_THREE" | bc -l) ))
		then
		STEP_MASS=0.00005
	fi

	# for alpha in 1.00 1.10 1.20 1.30 1.40 1.50 1.60 1.70
	# for alpha in 1.80 1.90 2.00 2.10 2.20 2.30 2.40 2.50
	for alpha in 1.85

	do
		a=$alpha
		echo $a

		echo "Mass: $m, Metallicity: $z, alpha_mlt: $a, initial_y: $y"

		
		sbatch PAPER_mass_evo.sh $m $z $a $y
		
		#Increment count for jobs per batch
		count=$((count + 1))
		sleep 1
	done

	m=$(echo "scale=10; $m + $STEP_MASS" | bc)
done

