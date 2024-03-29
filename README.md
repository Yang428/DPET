# DPET - Dynamical Position Embedding based Tracking framework

## Publication
Yijin Yang and Xiaodong Gu.
Learning Dynamical Position Embedding for Discriminative Segmentation Tracking.
TITS, 2024. [[paper]](https://ieeexplore.ieee.org/document/10409135)

# Abstract
Visual tracking plays a pivotal role in intelligent transportation systems and has a wide range of practical applications such as autonomous driving and traffic counting. Recently, the attention mechanism in Transformers has been successfully applied to the field of visual tracking, leading to a significant improvement in tracking performance. However, Transformer-based trackers directly flatten two-dimensional image features into one-dimensional vectors to compute attention scores. This process unavoidably results in the omission of crucial position distribution information necessary for precise target localization. To address this issue, we propose a novel cross-attention based tracking-by-segmentation framework, called Dynamical Position Embedding based Tracking framework (DPET). DPET incorporates an additional network for modeling position information to complement the cross-attention module. To be specific, a dynamical position embedding network is introduced to adaptively encode position information. This network is then integrated into the cross-attention based feature fusion network to compensate for the loss of position distribution information. As a result, the fused feature incorporates abundant contextual semantic cues for target classification and precise position information for target localization simultaneously. To overcome the constraints imposed by bounding-boxes, a segmentation network that takes the fused feature as input is designed to achieve accurate pixel-wise tracking. Extensive experiments on eight challenging tracking benchmarks show that our DPET tracker enables real-time operations and achieves promising tracking performance on the GOT-10K benchmark. Especially, DPET tracker achieves the top accuracy scores on VOT2016, VOT2018 and VOT2019 benchmarks.

## Demo
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/CarScale.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Ironman.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/DragonBaby.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Matrix.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/got4.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Deer.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Skating1.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Skating2_1.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Skating2_2.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Basketball.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Football.gif)
![image](https://github.com/Yang428/DPET/blob/master/resultsOnBenchmarks/Diving.gif)

## Running Environments
* Pytorch 1.1.0, Python 3.6.12, Cuda 9.0, torchvision 0.3.0, cudatoolkit 9.0, Matlab R2016b.
* Ubuntu 16.04, NVIDIA GeForce GTX 1080Ti.

## Installation
The instructions have been tested on an Ubuntu 16.04 system. In case of issues, we refer to these two links [1](https://github.com/alanlukezic/d3s) and [2](https://github.com/visionml/pytracking) for details.

#### Clone the GIT repository
```
git clone https://github.com/Yang428/DPET.git.
```

#### Install dependent libraries
Run the installation script 'install.sh' to install all dependencies. We refer to [this link](https://github.com/visionml/pytracking/blob/master/INSTALL.md) for step-by-step instructions.
```
bash install.sh conda_install_path pytracking
```

#### Or step by step install
```
conda create -n pytracking python=3.6
conda activate pytracking
conda install -y pytorch=1.1.0 torchvision=0.3.0 cudatoolkit=9.0 -c pytorch
conda install -y matplotlib=2.2.2
conda install -y pandas
pip install opencv-python
pip install tensorboardX
conda install -y cython
pip install pycocotools
pip install jpeg4py 
sudo apt-get install libturbojpeg
```

#### Or copy my environment directly.

You can download the packed conda environment from the [Baidu cloud link](https://pan.baidu.com/s/1gMQOB2Zs1UPj6n8qzJc4Lg?pwd=qjl2), the extraction code is 'qjl2'.

#### Download the pre-trained networks
You can download the models from the [Baidu cloud link](https://pan.baidu.com/s/1gDHbLW3DeiVkx7iHtitnAw?pwd=5sfo), the extraction code is '5sfo'. Then put the model files 'DPETNet.pth.tar' to the subfolder 'pytracking/networks'.

## Testing the tracker
There are the [raw resullts](https://github.com/Yang428/DPET/tree/master/resultsOnBenchmarks) on eight datasets. 
1) Download the testing datasets OTB-100, LaSOT, Got-10k, TrackingNet, VOT2016, VOT2018, VOT2019, VOT2020 and VOT2021 from the following Baidu cloud links.
* [OTB-100](https://pan.baidu.com/s/1TC6BF9erhDCENGYElfS3sw), the extraction code is '9x8q'.
* [LaSOT](https://pan.baidu.com/s/1KBlrWGOFH9Fe85pCWN5ZkA&shfl=sharepset#list/path=%2F).
* [Got-10k](https://pan.baidu.com/s/1t_PvpIicHc0U9yR4upf-cA), the extraction code is '78hq'.
* [TrackingNet](https://pan.baidu.com/s/1BKtc4ndh_QrMiXF4fBB2sQ), the extraction code is '5pj8'.
* [VOT2016](https://pan.baidu.com/s/1iU88Aqq9mvv9V4ZwY4gUuw), the extraction code is '8f6w'.
* [VOT2018](https://pan.baidu.com/s/1ztAfNwahpDBDssnEYONDuw), the extraction code is 'jsgt'.
* [VOT2019](https://pan.baidu.com/s/1vf7l4sQMCxZY_fDsHkuwTA), the extraction code is '61kh'.
* [VOT2020](https://pan.baidu.com/s/16PFiEdnYQDIGh4ZDxeNB_w), the extraction code is 'kdag'.
* [VOT2021](https://votchallenge.net/vot2021/dataset.html)
* Or you can download almost all tracking datasets from this web [link](https://blog.csdn.net/laizi_laizi/article/details/105447947#VisDrone_77).

2) Change the following paths to you own paths.
```
Network path: pytracking/parameters/dpet/dpet.py  params.segm_net_path.
Results path: pytracking/evaluation/local.py  settings.network_path, settings.results_path, dataset_path.
```
3) Run the DPET tracker on OTB-100, LaSOT, Got10k and TrackingNet datasets.
```
cd pytracking
python run_experiment.py myexperiments otb
python run_experiment.py myexperiments lasot
python run_experiment.py myexperiments got10k
python run_experiment.py myexperiments trackingnet
```

## Evaluation on VOT16, VOT18 and VOT19 using Matlab R2016b
We provide a [VOT Matlab toolkit](https://github.com/votchallenge/toolkit-legacy) integration for the DPET tracker. There is the [tracker_DPET.m](https://github.com/Yang428/DPET/tree/master/pytracking/utils) Matlab file in the 'pytracking/utils', which can be connected with the toolkit. It uses the 'pytracking/vot_wrapper.py' script to integrate the tracker to the toolkit.

## Evaluation on VOT2020 and VOT2021 using Python Toolkit
We provide a [VOT Python toolkit](https://github.com/votchallenge/toolkit) integration for the DPET tracker. There is the [trackers.ini](https://github.com/Yang428/DPET/tree/master/pytracking/utils) setting file in the 'pytracking/utils', which can be connected with the toolkit. It uses the 'pytracking/vot20_wrapper.py' script to integrate the tracker to the toolkit.
```
cd pytracking/workspace_vot2020 (or workspace_vot2021)
pip install git+https://github.com/votchallenge/vot-toolkit-python
vot initialize <vot2020> --workspace ./workspace_vot2020/
vot evaluate DPET
vot analysis --workspace ./workspace_vot2020/DPET
```

## Training the networks
The DPET network is trained on the YouTube VOS, GOT-10K and LaSOT datasets. Download the VOS training dataset (2018 version) and copy the files vos-list-train.txt and vos-list-val.txt from ltr/data_specs to the training directory of the VOS dataset. Download the bounding boxes from [this link](http://data.vicos.si/alanl/d3s/rectangles.zip) and copy them to the corresponding training sequence directories.
1) Download the YouTube VOS dataset from [this link](https://youtube-vos.org/challenge/2018/).
2) Download the GOT-10K dataset from [this link](https://blog.csdn.net/laizi_laizi/article/details/105447947#VisDrone_77).
3) Download the LaSOT dataset from [this link](https://blog.csdn.net/laizi_laizi/article/details/105447947#VisDrone_77).
4) Download the pre-generated masks of GOT-10K and LaSOT from [link 1](https://drive.google.com/file/d/17YcdQOoA4DubK-krClJfxNtw9ooCyWHv/view) or [link 2](https://pan.baidu.com/s/1YrxdGr5VPqwDen7gOK-j4A?pwd=p1vu). We refer to [RTS](https://github.com/visionml/pytracking/blob/master/ltr/README.md#RTS) for more instructions.

5) Change the following paths to you own paths.
```
Workspace: ltr/admin/local.py  workspace_dir.
Dataset: ltr/admin/local.py  vos_dir.
Pre_masks: ltr/admin/local.py  pregenerated_masks
```
3) Taining the DPET network
```
cd ltr
python run_training.py dpet dpet_default
```

## Acknowledgement
We would like to thank the author Martin Danelljan of [pytracking](https://github.com/visionml/pytracking) and the author Alan Lukežič of [D3S](https://github.com/alanlukezic/d3s).


## <b>BibTex citation:</b></br>
@ARTICLE{Yijin2024,<br>
title = {Learning Dynamical Position Embedding for Discriminative Segmentation Tracking},<br>
author = {Yijin, Yang. and Xiaodong, Gu.},<br>
journal = {TITS},<br>
volume  = {},<br>
pages = {},<br>
year    = {2024},<br>
doi = {10.1109/TITS.2024.3350673}<br>
}
