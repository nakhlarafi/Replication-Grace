# This scripts sets up all the initialization for running defects4j
work_dir="/Users/tahminaakter/Desktop/test/newVtest/defect"


export _JAVA_OPTIONS="-Xmx6144M -XX:MaxHeapSize=4096M"
export MAVEN_OPTS="-Xmx1024M"
export ANT_OPTS="-Xmx6144M -XX:MaxHeapSize=4096M"


cd "$work_dir"
git clone https://github.com/GZoltar/gzoltar.git
cd "$work_dir/gzoltar"
mvn clean package

export GZOLTAR_AGENT_JAR="$work_dir/gzoltar/com.gzoltar.agent.rt/target/com.gzoltar.agent.rt-1.7.4-SNAPSHOT-all.jar"
export GZOLTAR_CLI_JAR="$work_dir/gzoltar/com.gzoltar.cli/target/com.gzoltar.cli-1.7.4-SNAPSHOT-jar-with-dependencies.jar"



cd "$work_dir"
# git clone https://github.com/rjust/defects4j.git
cd "$work_dir/defects4j-1.2.0"
./init.sh

export D4J_HOME="$work_dir/defects4j-1.2.0"
export TZ='America/Los_Angeles'
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
