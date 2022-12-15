# This script runs the Defect4j coverage command for all the projects
# Usage . ./run_coverage_gzoltar.sh Lang

work_dir="/Users/tahminaakter/Desktop/test/newVtest/defect/"



PID=$1
for i in {1..65}
do
    BID="$i"
    cd "$work_dir/$PID-${BID}b"
    "defects4j" coverage -i all-classes.txt
    cd ..
done