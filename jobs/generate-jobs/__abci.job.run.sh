#!/usr/bin/env bash
module load spack
module load cuda/10.1

export LOCAL_HOME=$HOME/local
export LD_LIBRARY_PATH=$LOCAL_HOME/lib
export LD_LIBRARY_PATH=$MPIROOT/lib:$LD_LIBRARY_PATH
export MANPATH=$MANPATH:$MPIROOT/share/man

echo PATH=$PATH

LD_PATH=$HOME/local/cuda-10.1/lib64:$MPIROOT/lib64:$(echo $LD_LIBRARY_PATH)
export LD_LIBRARY_PATH=$LD_PATH

echo LD_LIBRARY_PATH=$LD_LIBRARY_PATH
echo LOCAL_PATH=$LOCAL_HOME
echo HOME=$HOME

PY=$(which python3)
mode=bin
process_name=karma

echo PY=$PY
echo process_name=$process_name
#############################

