#!/bin/sh
# This script runs the gzoltar fault localization process.
# Usage . ./gzoltar_test.sh Lang

work_dir="/Users/tahminaakter/Desktop/test/newVtest/defect"


# export _JAVA_OPTIONS="-Xmx6144M -XX:MaxHeapSize=4096M"
# export MAVEN_OPTS="-Xmx1024M"
# export ANT_OPTS="-Xmx6144M -XX:MaxHeapSize=4096M"


# cd "$work_dir"
# git clone https://github.com/GZoltar/gzoltar.git
# cd "$work_dir/gzoltar"
# mvn clean package

# export GZOLTAR_AGENT_JAR="$work_dir/gzoltar/com.gzoltar.agent.rt/target/com.gzoltar.agent.rt-1.7.4-SNAPSHOT-all.jar"
# export GZOLTAR_CLI_JAR="$work_dir/gzoltar/com.gzoltar.cli/target/com.gzoltar.cli-1.7.4-SNAPSHOT-jar-with-dependencies.jar"



# cd "$work_dir"
# # git clone https://github.com/rjust/defects4j.git
# cd "$work_dir/defects4j"
# ./init.sh

# export D4J_HOME="$work_dir/defects4j"
# export TZ='America/Los_Angeles'
# export LC_ALL=en_US.UTF-8
# export LANG=en_US.UTF-8
# export LANGUAGE=en_US.UTF-8

for i in {21..41}
do
    PID=$1
    BID="$i"


    cd "$work_dir"
    #rm -rf "$PID-${BID}b"; "defects4j" checkout -p "$PID" -v "${BID}b" -w "$PID-${BID}b"


    cd "$work_dir/$PID-${BID}b"
    "defects4j" compile


    cd "$work_dir/$PID-${BID}b"
    test_classpath=$(defects4j export -p cp.test)
    src_classes_dir=$(defects4j export -p dir.bin.classes)
    src_classes_dir="$work_dir/$PID-${BID}b/$src_classes_dir"
    test_classes_dir="target/test-classes"
    test_classes_dir="$work_dir/$PID-${BID}b/$test_classes_dir"
    echo "$PID-${BID}b's classpath: $test_classpath" >&2
    echo "$PID-${BID}b's bin dir: $src_classes_dir" >&2
    echo "$PID-${BID}b's test bin dir: $test_classes_dir" >&2


    cd "$work_dir/$PID-${BID}b"
    unit_tests_file="$work_dir/$PID-${BID}b/unit_tests.txt"


    java -cp "$test_classpath:$test_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$GZOLTAR_CLI_JAR" \
    com.gzoltar.cli.Main listTestMethods \
        "$test_classes_dir" \
        --outputFile "$unit_tests_file" 
    head "$unit_tests_file"


    cd "$work_dir/$PID-${BID}b"

    loaded_classes_file="$D4J_HOME/framework/projects/$PID/loaded_classes/$BID.src"
    normal_classes=$(cat "$loaded_classes_file" | sed 's/$/:/' | sed ':a;N;$!ba;s/\n//g')
    inner_classes=$(cat "$loaded_classes_file" | sed 's/$/$*:/' | sed ':a;N;$!ba;s/\n//g')
    classes_to_debug="$normal_classes$inner_classes"
    echo "Likely faulty classes: $classes_to_debug" >&2


    cd "$work_dir/$PID-${BID}b"

    ser_file="$work_dir/$PID-${BID}b/gzoltar.ser"
    java -XX:MaxPermSize=4096M -javaagent:$GZOLTAR_AGENT_JAR=destfile=$ser_file,buildlocation=$src_classes_dir,inclnolocationclasses=false,output="FILE" \
    -cp "$src_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$test_classpath:$GZOLTAR_CLI_JAR" \
    com.gzoltar.cli.Main runTestMethods \
        --testMethods "$unit_tests_file" \
        --collectCoverage


    cd "$work_dir/$PID-${BID}b"

    java -cp "$src_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$test_classpath:$GZOLTAR_CLI_JAR" \
        com.gzoltar.cli.Main faultLocalizationReport \
        --buildLocation "$src_classes_dir" \
        --granularity "line" \
        --inclPublicMethods \
        --inclStaticConstructors \
        --inclDeprecatedMethods \
        --dataFile "$ser_file" \
        --outputDirectory "$work_dir/$PID-${BID}b" \
        --family "sfl" \
        --formula "ochiai" \
        --metric "entropy" \
        --formatter "txt"


    cd ..
    cd ..
    done