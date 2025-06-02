#!/bin/bash

# ----------- Argument validation ----------- #
NRUNS=$1
SEED=$2
NCORES=20

if [[ -z "$NRUNS" || ! "$NRUNS" =~ ^[0-9]+$ ]]; then
    echo "Usage: $0 <NRUNS> [SEED]"
    echo "NRUNS must be a positive integer."
    exit 1
fi

# ----------- Generate random seed if not provided ----------- #
if [[ -z "$SEED" ]]; then
    SEED=$(date +%s%N | cut -b1-9)  # Nano timestamp, first 9 digits
    echo "[INFO] No seed provided. Generated random seed: $SEED"
fi

# ----------- Define output folder using timestamp and seed ----------- #
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_PATH="output/run_${TIMESTAMP}_seed${SEED}/"

echo "[INFO] Creating output directories..."
mkdir -p "$OUTPUT_PATH" "$OUTPUT_PATH/main_files" "$OUTPUT_PATH/inputs_tmp" "$OUTPUT_PATH/logs"

inputs_tmp="$OUTPUT_PATH/inputs_tmp"
main_files="$OUTPUT_PATH/main_files"
logs="$OUTPUT_PATH/logs"

# ----------- Save execution parameters ----------- #
{
    echo "NRUNS=$NRUNS"
    echo "SEED=$SEED"
    echo "TIMESTAMP=$TIMESTAMP"
    echo "NCORES=$NCORES"
} > "$OUTPUT_PATH/run_info.txt"

# ----------- Determine max concurrent jobs ----------- #
MAX_JOBS=$(( NRUNS < NCORES ? NRUNS : NCORES ))

echo "[INFO] Running $NRUNS simulations with up to $MAX_JOBS concurrent jobs..."
echo "[INFO] Output will be saved in: $OUTPUT_PATH"

# ----------- Launch simulation jobs ----------- #
for ((nj=0; nj<NRUNS; nj++)); do
    SUFFIX=$nj
    echo "[INFO] Launching job $nj with suffix $SUFFIX..."

    # Create customized GetImage_$SUFFIX.in
    awk -v SUFFIX=$SUFFIX -v OUTPUT_PATH=$OUTPUT_PATH '{
        if ($2=="GetImage:ResultsFolder") {
            printf("/gamos/setParam GetImage:ResultsFolder %s\n", OUTPUT_PATH)
        } else if ($2=="GetImage:OutputFilename") {
            printf("/gamos/setParam GetImage:OutputFilename image_%s\n", SUFFIX)
        } else {
            print $0
        }
    }' inputs/GetImage.in > "$inputs_tmp/GetImage_$SUFFIX.in"

    # Compute unique seeds
    seed1=$((SEED + 2 * nj))
    seed2=$((SEED + 2 * nj + 1))

    # Create customized main_$SUFFIX.inn
    awk -v SUFFIX=$SUFFIX -v s1=$seed1 -v s2=$seed2 -v TMP_INPUTS=$inputs_tmp '{
        if ($2=="inputs/GetImage.in") {
            printf("/control/execute %s/GetImage_%s.in\n", TMP_INPUTS, SUFFIX)
        } else if ($1=="/gamos/random/setSeeds") {
            printf("/gamos/random/setSeeds %s %s\n", s1, s2)
        } else {
            print $0
        }
    }' main.in > "$main_files/main_$SUFFIX.inn"

    # Run simulation and log output
    gamos "$main_files/main_$SUFFIX.inn" 2>&1 | tee "$logs/log_main_$SUFFIX.log" &

    # Control number of concurrent jobs
    if [[ $(jobs -r -p | wc -l) -ge $MAX_JOBS ]]; then
        wait -n
    fi
done

wait

echo "[INFO] All simulations have completed."
echo "[INFO] Output directory: $OUTPUT_PATH"

# ----------- Prompt for cleanup ----------- #
echo ""
read -p "Do you want to delete the temporary files ($inputs_tmp and $main_files)? [y/N]: " answer

if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    echo "[INFO] Deleting temporary files..."
    rm -rf "$inputs_tmp" "$main_files"
    echo "[INFO] Temporary files deleted."
else
    echo "[INFO] Temporary files kept."
fi
