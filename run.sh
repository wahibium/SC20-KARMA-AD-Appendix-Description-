#!/bin/bash

# for scaling evaluation on abci hpc

# repeate N times

N=1

echo "#########################"
echo "each job repeat $N times"
jobs="resnet50 resnet200 resnet1001 wrn vgg16 megatron"

function run_job(){
	pushd jobs/get-datasets
		./clear.sh
		python3 gen-jobs.py $1
	popd
}


echo $#

for s in resnet50 resnet200 resnet1001 wrn vgg16 megatron; do	
	if [ $# -eq 1 ]; then
		if [ "$s" == "$1" ]; then
			echo "run all models : $s"
		else
			continue
		fi
	fi
	run_job $s
	batch-sub-jobs.sh $N

	echo "$s result is in folder test"
	mkdir -p test
	mkdir -p test/$s
	mv *.t1 test/$s
	mv *.t2 test/$s
	mv abci.job.run.* test$s
done




