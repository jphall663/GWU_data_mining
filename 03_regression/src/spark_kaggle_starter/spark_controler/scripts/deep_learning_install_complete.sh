#!/bin/bash


# enable debugging & set strict error trap
set -x -e


# change Home directory
export HOME=/mnt/home

mkdir /mnt/cuda
export CUDA_ROOT=/mnt/cuda
mkdir /mnt/tmp
export TMP_DIR=/mnt/tmp

# source script specifying environment variables
source ~/.EnvVars


# change directory to Temp folder to install NVIDIA driver & CUDA toolkit
cd $TMP_DIR


# install NVIDIA driver
# (ref: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using_cluster_computing.html#install-nvidia-driver)
# G2 Instances
# Product Type: GRID
# Product Series: GRID Series
# Product: GRID K520
# Operating System: Linux 64-bit
# Recommended/Beta: Recommended/Certified
wget http://us.download.nvidia.com/XFree86/Linux-x86_64/367.27/NVIDIA-Linux-x86_64-367.27.run
set +e
sudo sh NVIDIA-Linux-x86_64-367.27.run --silent --kernel-source-path $KERNEL_SOURCE_PATH --tmpdir $TMP_DIR
set -e
echo `df -h / | sed -n 2p` NVIDIA >> $MAIN_DISK_USAGE_LOG


# install CUDA toolkit
wget http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run
sudo sh cuda_7.5.18_linux.run --silent --driver --toolkit --toolkitpath $CUDA_ROOT --extract $TMP_DIR --kernel-source-path $KERNEL_SOURCE_PATH --tmpdir $TMP_DIR
sudo sh cuda-linux64-rel-7.5.18-19867135.run --noprompt --prefix $CUDA_ROOT --tmpdir $TMP_DIR

# add CUDA executables & libraries to Path
# instructions: Please make sure that
# -   PATH includes /mnt/cuda-7.5/bin
# -   LD_LIBRARY_PATH includes /mnt/cuda-7.5/lib64, or,
# add /mnt/cuda-7.5/lib64 to /etc/ld.so.conf and run ldconfig as root
echo "$CUDA_ROOT/lib64" > cuda.conf
echo "$CUDA_ROOT/lib"  >> cuda.conf
sudo mv cuda.conf /etc/ld.so.conf.d/
sudo ldconfig

# create symbolic links for NVCC
sudo ln -s $CUDA_ROOT/bin/nvcc /usr/bin/nvcc

# copy link stubs (?) to /usr/bin directory
sudo cp -r $CUDA_ROOT/bin/crt/ /usr/bin/

echo `df -h / | sed -n 2p` CUDA Toolkit >> $MAIN_DISK_USAGE_LOG


wget https://raw.githubusercontent.com/ChicagoBoothAnalytics/Software/master/NVIDIA/cudnn-7.5-linux-x64-v5.0-ga.tgz
tar xvzf cudnn-*.tgz
sudo rm cudnn-*.tgz
sudo mv cudnn-*/cudnn.h $CUDA_ROOT/include
sudo mv cudnn-*/libcudnn* $CUDA_ROOT/lib64
sudo chmod a+r $CUDA_ROOT/include/cudnn.h $CUDA_ROOT/lib64/libcudnn*
sudo rm -r cudnn-*

echo `df -h / | sed -n 2p` CuDNN >> $MAIN_DISK_USAGE_LOG


# change directory to Programs directory
cd $APPS_DIR


# install OpenBLAS
git clone https://github.com/xianyi/OpenBLAS $OPENBLAS_DIR
cd $OPENBLAS_DIR
make
sudo make install PREFIX=$OPENBLAS_DIR
echo `df -h / | sed -n 2p` OpenBLAS >> $MAIN_DISK_USAGE_LOG
cd $APPS_DIR

# skip installation of GotoBLAS2 because of error: https://gist.github.com/certik/1224558
# cd $APPS_DIR
# wget https://www.tacc.utexas.edu/documents/1084364/1087496/GotoBLAS2-1.13.tar.gz
# tar xzf GotoBLAS2-1.13.tar.gz
# sudo rm GotoBLAS2-1.13.tar.gz
# cd GotoBLAS2
# make
# sudo make install PREFIX=$GOTOBLAS_DIR
# cd ..
# sudo rm -r GotoBLAS2


# install CUDA-related packages
git clone --recursive http://git.tiker.net/trees/pycuda.git
cd pycuda
sudo python configure.py --cuda-root=$CUDA_ROOT
set +e
sudo make install
set -e
cd ..
sudo rm -r pycuda
echo `df -h / | sed -n 2p` PyCUDA >> $MAIN_DISK_USAGE_LOG

# sudo pip install git+https://github.com/cudamat/cudamat.git   installation fails
# git clone https://github.com/cudamat/cudamat.git
# cd cudamat
# sudo python setup.py install
# cd ..
# sudo rm -r cudamat
# echo `df -h / | sed -n 2p` CUDAmat >> $MAIN_DISK_USAGE_LOG

git clone https://github.com/andersbll/cudarray
cd cudarray
make
sudo make install
sudo python setup.py install
cd ..
sudo rm -r cudarray
echo `df -h / | sed -n 2p` CUDArray >> $MAIN_DISK_USAGE_LOG

set +e
sudo pip install --upgrade SciKit-CUDA
set -e
echo `df -h / | sed -n 2p` SciKit-CUDA >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade GNumPy
echo `df -h / | sed -n 2p` GNumPy >> $MAIN_DISK_USAGE_LOG


# install TensorFlow
sudo pip install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.9.0-cp27-none-linux_x86_64.whl
echo `df -h / | sed -n 2p` TensorFlow >> $MAIN_DISK_USAGE_LOG


# install Theano
sudo pip install --upgrade Theano
echo `df -h / | sed -n 2p` Theano >> $MAIN_DISK_USAGE_LOG

# download .TheanoRC into new Home directory
cd ~
wget $GITHUB_REPO_RAW_PATH/.config/$THEANORC_SCRIPT_NAME
dos2unix $THEANORC_SCRIPT_NAME
cd $APPS_DIR


# install HDF5
sudo yum install -y https://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.16/bin/RPMS/hdf5-1.8.16-1.with.szip.encoder.el7.x86_64.rpm https://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.16/bin/RPMS/hdf5-devel-1.8.16-1.with.szip.encoder.el7.x86_64.rpm
echo `df -h / | sed -n 2p` HDF5 >> $MAIN_DISK_USAGE_LOG


# install Tables
git clone https://github.com/PyTables/PyTables
cd PyTables
sudo python setup.py install
cd ..
sudo rm -r PyTables
echo `df -h / | sed -n 2p` Tables >> $MAIN_DISK_USAGE_LOG


# install Deep Learning packages
sudo pip install git+git://github.com/mila-udem/fuel.git   # don't use --upgrade: PyTables messing up...
echo `df -h / | sed -n 2p` Fuel >> $MAIN_DISK_USAGE_LOG

sudo pip install git+git://github.com/mila-udem/blocks.git   # don't use --upgrade: PyTables messing up...
echo `df -h / | sed -n 2p` Blocks >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade git+https://github.com/mila-udem/platoon
echo `df -h / | sed -n 2p` Platoon >> $MAIN_DISK_USAGE_LOG

set +e
sudo pip install --upgrade Brainstorm[all]
set -e
echo `df -h / | sed -n 2p` Brainstorm >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade Chainer
echo `df -h / | sed -n 2p` Chainer >> $MAIN_DISK_USAGE_LOG

git clone https://github.com/akrizhevsky/cuda-convnet2

# sudo pip install --upgrade DeepCL   SKIPPED: needs OpenCL

sudo pip install DeepDish   # don't use --upgrade: PyTables messing up...
echo `df -h / | sed -n 2p` DeepDish >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade git+git://github.com/dirkneumann/deepdist.git   # abandoned project
echo `df -h / | sed -n 2p` DeepDist >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade git+git://github.com/andersbll/deeppy.git
echo `df -h / | sed -n 2p` DeepPy >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade Deepy
echo `df -h / | sed -n 2p` Deepy >> $MAIN_DISK_USAGE_LOG

git clone https://github.com/libfann/fann.git
cd fann
cmake .
sudo make install
cd ..
sudo rm -r fann
sudo pip install --upgrade FANN2
echo `df -h / | sed -n 2p` FANN2 >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade FFnet
echo `df -h / | sed -n 2p` FFnet >> $MAIN_DISK_USAGE_LOG

set +e
sudo pip install --upgrade Hebel
set -e
echo `df -h / | sed -n 2p` Hebel >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade Keras
echo `df -h / | sed -n 2p` Keras >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
echo `df -h / | sed -n 2p` Lasagne >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade Mang   # abandoned project
# echo `df -h / | sed -n 2p` Mang >> $MAIN_DISK_USAGE_LOG

git clone https://github.com/dmlc/minerva
cd minerva
sudo cp configure.in.example configure.in
# then we need to manually edit CONFIGURE.IN and run below steps
# ./build.sh
cd $APPS_DIR

sudo pip install --upgrade git+git://github.com/hycis/Mozi.git
echo `df -h / | sed -n 2p` Mozi >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade NervanaNEON
echo `df -h / | sed -n 2p` NervanaNEON >> $MAIN_DISK_USAGE_LOG

sudo pip install NeuralPy   # don't use --upgrade: it'd downgrade NumPy
echo `df -h / | sed -n 2p` NeuralPy >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade NeuroLab
echo `df -h / | sed -n 2p` NeuroLab >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade NLPnet
echo `df -h / | sed -n 2p` NLPnet >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade git+git://github.com/zomux/nlpy.git
echo `df -h / | sed -n 2p` NLPy >> $MAIN_DISK_USAGE_LOG

# sudo pip install --upgrade NN   # SKIPPED: toy project
# echo `df -h / | sed -n 2p` NN >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade NoLearn
echo `df -h / | sed -n 2p` NoLearn >> $MAIN_DISK_USAGE_LOG

wget http://bitbucket.org/eigen/eigen/get/3.2.8.zip
unzip 3.2.8.zip
sudo rm 3.2.8.zip
mkdir eigen-build
cd eigen-build
cmake $APPS_DIR/eigen-eigen-*
sudo make install
cd $APPS_DIR
sudo rm -r eigen*
echo `df -h / | sed -n 2p` Eigen >> $MAIN_DISK_USAGE_LOG

git clone https://github.com/OpenANN/OpenANN.git
cd OpenANN
mkdir build
cd build
cmake ..
sudo make install
sudo ldconfig
cd $APPS_DIR
sudo rm -r OpenANN
sudo mv /usr/local/local/lib64/python2.7/site-packages/* /usr/local/lib64/python2.7/site-packages/
echo `df -h / | sed -n 2p` OpenANN >> $MAIN_DISK_USAGE_LOG

# git clone https://github.com/guoding83128/OpenDL   SKIPPED: abandoned project
# echo `df -h / | sed -n 2p` OpenDL >> $MAIN_DISK_USAGE_LOG

git clone https://github.com/vitruvianscience/opendeep.git
cd opendeep
sudo python setup.py develop
cd ..

sudo pip install --upgrade PyBrain
echo `df -h / | sed -n 2p` PyBrain >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade PyBrain2
echo `df -h / | sed -n 2p` PyBrain2 >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade PyDeepLearning
echo `df -h / | sed -n 2p` PyDeepLearning >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade PyDNN
echo `df -h / | sed -n 2p` PyDNN >> $MAIN_DISK_USAGE_LOG

git clone git://github.com/lisa-lab/pylearn2.git
cd pylearn2
sudo python setup.py develop
cd ..

sudo pip install --upgrade PythonBrain
echo `df -h / | sed -n 2p` PythonBrain >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade SciKit-NeuralNetwork
echo `df -h / | sed -n 2p` SciKit-NeuralNetwork >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade git+git://github.com/google/SKFlow.git
echo `df -h / | sed -n 2p` SKFlow >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade git+git://github.com/sklearn-theano/sklearn-theano
echo `df -h / | sed -n 2p` SKLearn-Theano >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade git+git://github.com/dougefr/Synapyse.git
echo `df -h / | sed -n 2p` Synapyse >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade Theanets
echo `df -h / | sed -n 2p` Theanets >> $MAIN_DISK_USAGE_LOG

sudo pip install --upgrade git+git://github.com/Samsung/veles.git
echo `df -h / | sed -n 2p` Veles >> $MAIN_DISK_USAGE_LOG

git clone https://github.com/Samsung/veles.znicz
