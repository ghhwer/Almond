#!/bin/bash

if [[ $SPARK_MODE == "WORKER" ]]
then
    echo "Starting in WORKER mode"
    . "$SPARK_HOME/sbin/spark-config.sh"
    . "$SPARK_HOME/bin/load-spark-env.sh"
    mkdir -p $SPARK_LOGS
    ln -sf /dev/stdout $SPARK_LOGS/spark-worker.out

    $SPARK_HOME/sbin/../bin/spark-class org.apache.spark.deploy.worker.Worker \
        --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER >> $SPARK_LOGS/spark-worker.out
elif [[ $SPARK_MODE == "MASTER" ]]
then
    echo "Starting in MASTER mode"
    export SPARK_MASTER_HOST=${SPARK_MASTER_HOST:-`hostname`}
    . "$SPARK_HOME/sbin/spark-config.sh"
    . "$SPARK_HOME/bin/load-spark-env.sh"
    mkdir -p $SPARK_LOGS
    ln -sf /dev/stdout $SPARK_LOGS/spark-master.out

    $SPARK_HOME/sbin/../bin/spark-class org.apache.spark.deploy.master.Master \
      --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT >> $SPARK_LOGS/spark-master.out  
else
  echo "No mode was set :("
fi
