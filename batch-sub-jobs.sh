#!/bin/sh

JOBS=$(ls ./jobs/abci.job.run.*)
echo $JOBS


#### Add group ID assinged by ABCI
GROUPID=

N=1
if [ "$#" -gt 0 ]; then
        N=$1
fi
echo repeat count : N=$N

function has_jobs(){
        s=$(qstat | grep $(whoami))
        if [ -z "$s" ] ; then
                echo "1"
        else
                echo "0"
        fi
}
function wait_jobs(){
        count=4
        sleep 1
        while [ $(has_jobs) = 0 ]; do
                printf "\rwait ...$count s"
                sleep 4
                count=$((count+4))
        done
        printf "\n"
}
#echo has_jobs=$(has_jobs)
for ((i=1; i<=$N; i++)); do
        echo ####### $i ######
        for S in $JOBS; do
                echo job_name=$S
                rm -rf ~/dump/* && qsub -g $GROUPID $S
                wait_jobs
        done
done
