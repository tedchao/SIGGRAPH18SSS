## Important Note:
**This repository alone is not a complete code. Please also check the repository for segmentation part [[here](https://github.com/yaksoy/SemanticSoftSegmentation)].**

**Also, please readme README carefully.**

# Semantic Soft Segmentation, ACM SIGGRAPH 2018

This repository includes the semantic feature (128-D) generation approach presented in

    Yagiz Aksoy, Tae-Hyun Oh, Sylvain Paris, Marc Pollefeys and Wojciech Matusik, "Semantic Soft Segmentation", ACM Transactions on Graphics (Proc. SIGGRAPH), 2018 

Also, note that this repository is NOT **stand-alone**. 
The spectral segmentation implementation can be found [[here](https://github.com/yaksoy/SemanticSoftSegmentation)].
The low-dimension projection to 3-dimension and its filtering code are available in the repository.

Please refer to the [[project page](http://people.inf.ethz.ch/aksoyy/sss/)] for more information.

Note that only the feature generator is presented in this repository and the training code is not included.

# Requirements
Python 3.6, 1.8 >= TensorFlow >= 1.4 and other common packages listed in requirements.txt.

The code has been tested on {Linux Ubuntu 16.04, TensorFlow-GPU 1.4} and {Windows 10, TensorFlow-GPU 1.8} with Titan Xp.

# Installation
1. Install dependencies
```
pip3 install -r requirements.txt
pip install --upgrade tf_slim
```
2. Clone or download this repository.
3. Download the [pre-trained](http://cvg.ethz.ch/research/semantic-soft-segmentation/SSS_model.zip) model. (Note: This link seems not to be working anymore. [Here](https://drive.google.com/drive/folders/1nRpcKNO5BnpLbA8gi7neJPwIDUgh8quz?usp=sharing) is another link for downloading the pre-trained model.)
5. Extract the model and put the extracted "model" folder into the folder where the repository is cloned.
   - e.g., If the repository is cloned at "/project/sss", then move the model to be "/project/sss/model")
6. Run "run_extract_feat.sh", which will process sample images in the "samples" folder. If you want to run your own images, notice that image files should be the PNG formats.


# Notes
Currently, the code only supports the PNG file format.

# Citation
If you use this code, please cite our paper:

```
@ARTICLE{sss,
author={Ya\u{g}{\i}z Aksoy and Tae-Hyun Oh and Sylvain Paris and Marc Pollefeys and Wojciech Matusik},
title={Semantic Soft Segmentation},
journal={ACM Transactions on Graphics (Proc. SIGGRAPH)},
year={2018},
pages = {72:1-72:13},
volume = {37},
number = {4}
}
```
This code is for protyping research ideas; thus, please use this code only for non-commercial purpose only.  

# Credits
The part of the base codes (the tools in the "deeplab_resnet" directory) are borrowed from [(Re-)implementation of DeepLab-ResNet-TensorFlow](https://github.com/DrSleep/tensorflow-deeplab-resnet#using-your-dataset)
Likewise, our code (the tools in "kaffe" directory) is benefited from [Caffe to TensorFlow](https://github.com/ethereon/caffe-tensorflow)

Also, our architecture is implemented on top of the base architecture, DeepLab-ResNet-101.

```
@article{CP2016Deeplab,
      title={DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs},
      author={Liang-Chieh Chen and George Papandreou and Iasonas Kokkinos and Kevin Murphy and Alan L Yuille},
      journal={arXiv:1606.00915},
      year={2016}
    }
```

