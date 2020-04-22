#!/bin/sh

#$-l rt_F=8
#$-cwd
#$-l h_rt=00:04:00

source /etc/profile.d/modules.sh

#!/usr/bin/env bash
module load intel-mpi/2018.2.199
module load cuda/10.1
module load pytorch

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

NP=32
NPP=4
ROWS=8
NX=2048
NY=2048
NZ=2048
NU=2048
NV=2048
PROJS=2048
SRC_DIR=./data/
DST_DIR=./dump/
MAX_PROJ_DB=32768
echo nprocess=$NP npernode=$NPP Rows=$ROWS NX=$NX NY=$NY NZ=$NZ NU=$NU NV=$NV PROJS=$PROJS
echo SRC_DIR=$SRC_DIR
echo DST_DIR=$DST_DIR
echo MAX_PROJ_DB=$MAX_PROJ_DB

$PY ./$mode/$process_name $NPP $ROWS $NX $NY $NZ $NU $NV $PROJS $SRC_DIR $DST_DIR $MAX_PROJ_DB
