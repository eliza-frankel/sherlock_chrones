#!/bin/bash
# JOB HEADERS HERE

#SBATCH --account=gr-isochronebldg
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=50G
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=efrankel@uwyo.edu


source ~/.bashrc
mesa
cd /project/gr-isochronebldg/efrankel/working/2025/FINAL_PAPER_EVERYTHING


#$1 == mass
#$2 == z
#$3 == alpha_mlt
#$4 == y

m=$(printf "%.8f" "$1")
z=$(printf "%.6f" "$2")
a=$(printf "%.2f" "$3")
y=$(printf "%.6f" "$4")


file=inlist_solo_template
newfile=${file%_template}_m${m}_z${z}_a${a}

sed -e "s/<<initial_mass>>/${m}/g" -e "s/<<initial_z>>/${z}/g" -e "s/<<initial_alpha>>/${a}/g" -e "s/<<initial_y>>/${y}/g" $file > $newfile
echo "Inlist submitted for m$1, z$2, a$3."

start_time=$(date +%Y-%m-%d_%H:%M:%S)
echo "Starting at $start_time"


./star $newfile > m$1_z$2_a$3.out



end_time=$(date +%Y-%m-%d_%H:%M:%S)
echo "Start time: $start_time" >> m$1_z$2_a$3.out
echo "End time: $end_time" >> m$1_z$2_a$3.out

rm $newfile

