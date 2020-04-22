## SC20 AD/AE for "Scaling Distributed Deep Learning Workloads beyond the Memory Capacity with KARMA"

We use ABCI (https://abci.ai/) HPC to apply an out-of-core solution for distributred DL training
This repository contains the artifact, e.g. job scripts, models, datasets.

#DEPENDENCIES

We tested on ABCI, using Nvidia Volta V100 GPUs, The following libraries and tools are requirements:

```
cmake = 3.1
CUDA = 10.1
python >= 3.5
PyTorch = 1.2 (built from source)
cuDNN = 7.6.1
Intel MPI 2018.2.199
```

#SOURCE CODE

Our Source Code is Closed (currenlty under review for open source licensing).

#MODELS
- For the first two (RestNet50, VGGA16), we load the from PyTorch model subpackges (torchvision.models) as follows:
```
import torchvision.models as models
resnet50 = models.resnet50()
vgg16 = models.vgg16()
```
- For ResNet200 we use the PyTroch implemenation at:
 https://github.com/osmr/imgclsmob/tree/master/pytorch
- For WRN-28-10 we use the PyTorch implementation at:
 https://github.com/szagoruyko/wide-residual-networks/tree/master/
- For Megatron-LM (with different congfigurations). We use the PyTorch implemention (original implementation by authors):
 https://github.com/NVIDIA/Megatron-LM


#DATASETS
- ImageNet:
http://www.image-net.org

- CIFAR-10:
https://www.cs.toronto.edu/~kriz/cifar.html

- OpenWebText (Open clone of OpenAI's unreleased WebText dataset scraper used to train Megatron-LM.)
https://github.com/jcpeterson/openwebtext

#RUNNING

all modules are in folder bin

Generating job script by running the script in the folder jobs/generate-jobs as
```
  python gen-jobs.py resnet50
  python gen-jobs.py resnet200
  python gen-jobs.py resnet1001
  python gen-jobs.py wrn
  python gen-jobs.py vgg16
  python gen-jobs.py megatron
```

Run jobs in the Root-folder of KARMA-artifact
```
  ./run.sh all
  ./run.sh resnet50
  ./run.sh resnet200
  ./run.sh resnet1001
  ./run.sh wrn
  ./run.sh vgg16
  ./run.sh megatron
Run models
```

Help/Support:

For more information or questions, contact the authors at wahibfy#gmail.com (replace # by @, please)
