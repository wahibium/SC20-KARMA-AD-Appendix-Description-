import os
from shutil import copyfile
import subprocess
import argparse
import math
import sys

abci_group_id = 'gaa50004'
src_dir ='./data/'
dst_dir ='./dump/'
MAX_PROJ_DB = 32768

base_path = "__abci.job.run.sh"

def generate_job(NP, NPP, ROWS, NX, NY, NZ, NU, NV, PROJS, SRC_DIR, DST_DIR, base):
	job_name = 'abci.job.run.%04d_%04d_%04d_%04d_%04d_%04d.sh' % (NP, NPP, ROWS, NX, NY, NZ)
	with open(base, 'r') as text_base:
		content = text_base.readlines()
		with open(job_name, "w") as text_file:
			text_file.write('#!/bin/sh\n')
			text_file.write('\n')
			text_file.write('#$-l rt_F=%d\n' % (NP/NPP) )
			text_file.write('#$-cwd\n')
			t = 2
			if NP >= 2048:   t = 6
			elif NP >= 1024: t = 5
			else:            t = 4
			text_file.write('#$-l h_rt=00:%02d:00\n' % (t))
			text_file.write('\n')
			text_file.write('source /etc/profile.d/modules.sh\n')
			text_file.write('\n')

			text_file.writelines(content)

			text_file.write('NP=%d\n' % NP)
			text_file.write('NPP=%d\n' % NPP)
			text_file.write('ROWS=%d\n' % ROWS)
			#text_file.write('VOL_SIZE=%d\n' % VOL_SIZE)
			text_file.write('NX=%d\n' % NX)
			text_file.write('NY=%d\n' % NY)
			text_file.write('NZ=%d\n' % NZ)
			text_file.write('NU=%d\n' % NU)
			text_file.write('NV=%d\n' % NV)
			text_file.write('PROJS=%d\n' % PROJS)
			text_file.write('SRC_DIR=%s\n' % SRC_DIR)
			text_file.write('DST_DIR=%s\n' % DST_DIR)
			text_file.write('MAX_PROJ_DB=%d\n' % MAX_PROJ_DB)

			text_file.write('echo nprocess=$NP npernode=$NPP Rows=$ROWS NX=$NX NY=$NY NZ=$NZ NU=$NU NV=$NV PROJS=$PROJS\n')
			text_file.write('echo SRC_DIR=$SRC_DIR\n')
			text_file.write('echo DST_DIR=$DST_DIR\n')
			text_file.write('echo MAX_PROJ_DB=$MAX_PROJ_DB\n\n')

			text_file.write('$PY ./$mode/$process_name $NPP $ROWS $NX $NY $NZ $NU $NV $PROJS $SRC_DIR $DST_DIR $MAX_PROJ_DB\n')
	return job_name


def sub_job(NP, NPP, ROWS, NX, NY, NZ, NU, NV, PROJS, SRC_DIR, DST_DIR, src=base_path):
	print("NP={},NPP={},ROWS={}, NX={}, NX={}, NX={}, PROJS={}".format(NP, NPP, ROWS, NX, NY, NZ, PROJS))
	#return
	if os.path.exists(src) == False:
		print 'Error : %s is not existed' % src
		return
	str = generate_job(NP, NPP, ROWS, NX, NY, NZ, NU, NV, PROJS, SRC_DIR, DST_DIR, src)
	#sub job
	#if os.path.exists(str):
	#	cmd = "qsub -g %s %s" % (str, abci_group_id)
	#	retcode = subprocess.call(cmd.split())
	#	print 'sub job {}, {}'.format(cmd, retcode)
	#else:
	#	print '%s is not existed\n'
	#

def single_gpu(S = 4):
	NU=2048
	NV=2048
	PROJS=4096
	SRC_DIR=src_dir
	DST_DIR=dst_dir
	index = 0
	for SCALE in [1, 2, 4, 8]:
		if S != SCALE:
			continue
		for ROWS in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
			#for i in range(0, 12):
			VOL_SIZE = 1024*SCALE
			#COLS = int(math.pow(2, i) + 0.5)
			COLS = 1
			if SCALE == 2:
				COLS = 4
			elif SCALE == 4:
				COLS = 32
			elif SCALE == 8:
				COLS = 256
			NP = COLS*ROWS
			if NP > 2048:
				continue
			NPP = 1
			if NP >= 4:
				NPP = 4
			elif NP >= 2:
				NPP = 2
			else:
				NPP = 1
			if (S != 8 & COLS*64 > VOL_SIZE):
				continue
			index += 1
			print "({}) : ".format(index)
			NPP = min(NP, NPP)
			sub_job(NP, NPP, ROWS, VOL_SIZE, VOL_SIZE, VOL_SIZE, NU, NV, PROJS, SRC_DIR, DST_DIR)


def multi_gpu(S=2):
	NP = 1
	NPP = 1

	VOL_SIZE = 1024*S
	#VOL_SIZE = 1024 * 2
	#VOL_SIZE = 1024 * 4
	NU=2048
	NV=2048
	#PROJS = 32
	#PROJS=8
	PROJS=8
	if S == 1:
		PROJS = 32
		NP = 1
	if S == 2:
		PROJS = 32*8
		NP = 4
	if S == 4:
		PROJS = 32*32
		NP = 32
	if S == 8:
		PROJS = 32*32
		NP = 256

	SRC_DIR=src_dir
	DST_DIR=dst_dir

	while True:
		if (NP > 2048):
			break
		if PROJS > MAX_PROJ_DB:
			break
		if NP <= 1:   NPP = 1
		elif NP <= 2: NPP = 2
		else:         NPP = 4

		#COLS = 1
		#COLS = 4
		#COLS = 32
		COLS = 1
		if (S == 2): COLS = 4
		if (S == 4): COLS = 32
		if (S == 8): COLS = 256

		for ROWS in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
			if ROWS*COLS != NP:
				continue
			if ROWS > NP:
				break
			NX=NY=NZ=VOL_SIZE
			sub_job(NP, NPP, ROWS, NX, NY, NZ, NU, NV, PROJS, SRC_DIR, DST_DIR)

		PROJS *= 2
		NP *= 2

def main():
	multi_gpu()
	#single_gpu()


if __name__ == "__main__":
	if len(sys.argv)  == 1:
		main()
	else:
		if sys.argv[1] == "resnet50":
			multi_gpu(2)
		elif sys.argv[1] == "resnet200":
			multi_gpu(4)
		elif sys.argv[1] == "resnet1001":
			multi_gpu(8)
		elif sys.argv[1] == "wrn":
			multi_gpu(2)
		elif sys.argv[1] == "vgg16":
			multi_gpu(4)
		elif sys.argv[1] == "megatron":
			multi_gpu(8)


