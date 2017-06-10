#!/usr/bin/env bash


# install conda (conda 4.2 defaults to python35)
wget --quiet http://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh -O ~/anaconda.sh \
    && /bin/bash ~/anaconda.sh -b -p $HOME/conda

echo -e '\nexport PATH=$HOME/conda/bin:$PATH' >> $HOME/.bashrc && source $HOME/.bashrc

# install packages
conda install -y ipython jupyter

#h2o uses pyqt4, downgrade
# conda install pyqt=4
conda update -y matplotlib
sudo yum install -y libXdmcp

# needed for PySparkling
# conda install requests
# conda install six
# conda install future
# conda install tabulate

#Install boto3 for AWS resource mgt
pip install boto3
# install pysparkling
pip install h2o
pip install h2o_pysparkling_2.1

#INSTALL SPARKLING WATER
# wget http://h2o-release.s3.amazonaws.com/sparkling-water/rel-2.1/8/sparkling-water-2.1.8.zip
# unzip sparkling-water-2.1.8.zip




# echo -e "\nexport PYSPARK_PYTHON=/home/hadoop/conda/bin/python" >> /etc/spark/conf/spark-env.sh
# echo "export PYSPARK_DRIVER_PYTHON=/home/hadoop/conda/bin/python" >> /etc/spark/conf/spark-env.sh

# #Thows Errors if all clusters don't have the same python hash seed as of python 3.2.3
# But need to set in Configurations script, can't set user env variables in bootstrap
# sudo export PYTHONHASHSEED=123
