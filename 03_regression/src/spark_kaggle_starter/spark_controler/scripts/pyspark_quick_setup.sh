#!/usr/bin/env bash

# bind conda to spark
echo -e "\nexport PYSPARK_PYTHON=/home/hadoop/conda/bin/python" >> /etc/spark/conf/spark-env.sh
echo "export PYSPARK_DRIVER_PYTHON=/home/hadoop/conda/bin/python" >> /etc/spark/conf/spark-env.sh
# echo "export PYSPARK_DRIVER_PYTHON=/home/hadoop/conda/bin/jupyter" >> /etc/spark/conf/spark-env.sh
# echo "export PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --ip=$1'" >> /etc/spark/conf/spark-env.sh
