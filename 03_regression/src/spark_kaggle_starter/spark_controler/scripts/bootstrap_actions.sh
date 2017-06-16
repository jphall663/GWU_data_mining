#!/usr/bin/env bash

# #Mounted directory we want to use
# export MOUNT_TO_USE=/mnt
#
# change Home directory
# mkdir $MOUNT_TO_USE/home
# export HOME=$MOUNT_TO_USE/home

# #For NVIDA installations
# mkdir $MOUNT_TO_USE/cuda
# export CUDA_ROOT=$MOUNT_TO_USE/cuda
# export CUDA_HOME=$CUDA_ROOT
# mkdir $MOUNT_TO_USE/tmp
# export TMP_DIR=$MOUNT_TO_USE/tmp

# #AWS AMI is based on RHEL and CentOS. So use one of those for installers
# wget http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run
# sudo sh cuda_7.5.18_linux.run --silent --verbose --toolkit --toolkitpath $CUDA_ROOT --tmpdir $TMP_DIR
# export LD_LIBRARY_PATH=$CUDA_ROOT/lib64${LD_LIBRARY_PATH:+:${LD_PATH}}
# export PATH=$CUDA_ROOT/bin${PATH:+:${PATH}}

# # Install cudnn
# wget https://s3.amazonaws.com/emr-related-files/cudnn-8.0-linux-x64-v5.1.tgz
# tar xvzf cudnn-8.0-linux-x64-v5.1.tgz
# cd cuda
# sudo cp include/cudnn.h $CUDA_HOME/include/
# sudo cp lib64/* $CUDA_HOME/lib64/

# pip install keras
# pip install tensorflow-gpu


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
# pip install h2o
pip install http://h2o-release.s3.amazonaws.com/h2o/rel-vapnik/1/Python/h2o-3.12.0.1-py2.py3-none-any.whl
pip install h2o_pysparkling_2.1

#install xgboost
pip install xgboost

#INSTALL SPARKLING WATER
# wget http://h2o-release.s3.amazonaws.com/sparkling-water/rel-2.1/8/sparkling-water-2.1.8.zip
# unzip sparkling-water-2.1.8.zip




# echo -e "\nexport PYSPARK_PYTHON=/home/hadoop/conda/bin/python" >> /etc/spark/conf/spark-env.sh
# echo "export PYSPARK_DRIVER_PYTHON=/home/hadoop/conda/bin/python" >> /etc/spark/conf/spark-env.sh

# #Thows Errors if all clusters don't have the same python hash seed as of python 3.2.3
# But need to set in Configurations script, can't set user env variables in bootstrap
# sudo export PYTHONHASHSEED=123
