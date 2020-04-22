#!/bin/sh



for s in resnet50 resnet200 resnet1001 wrn vgg16 megatron; do
	./clear.sh
	python gen-jobs.py $s
	mkdir -p ../$s
	rm -rf ../$s/*
	mv abci.job.run.* ../$s
done
