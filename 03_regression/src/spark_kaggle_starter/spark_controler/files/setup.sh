#!/bin/bash

# Parse arguments
s3_bucket="$1"
s3_bucket_script="$s3_bucket/script.tar.gz"

# Download compressed script tar file from S3
aws s3 cp $s3_bucket_script /home/hadoop/script.tar.gz

# Untar file
tar zxvf "/home/hadoop/script.tar.gz" -C /home/hadoop/

# Install requirements for Python script
# install conda
# sudo python2.7 -m pip install referer_parser

wget --quiet http://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh -O ~/anaconda.sh \
    && /bin/bash ~/anaconda.sh -b -p $HOME/conda

echo -e '\nexport PATH=$HOME/conda/bin:$PATH' >> $HOME/.bashrc && source $HOME/.bashrc

conda install -y ipython jupyter

echo -e "\nexport PYSPARK_PYTHON=/home/hadoop/conda/bin/python" >> /etc/spark/conf/spark-env.sh
echo "export PYSPARK_DRIVER_PYTHON=/home/hadoop/conda/bin/jupyter" >> /etc/spark/conf/spark-env.sh
echo "export PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --ip=$1'" >> /etc/spark/conf/spark-env.sh