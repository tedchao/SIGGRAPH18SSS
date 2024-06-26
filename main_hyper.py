"""
@author: Tae-Hyun Oh (http://taehyunoh.com, taehyun@csail.mit.edu)
@date: Jul 29, 2018
@description: This is a part of the semantic feature extraction implementation used in 
[Semantic Soft Segmentation (Aksoy et al., 2018)] (project page: http://people.inf.ethz.ch/aksoyy/sss/).
This code is modified from the implementation by DrSleep (https://github.com/DrSleep/tensorflow-deeplab-resnet)
This code is for protyping research ideas; thus, please use this code only for non-commercial purpose only.  
"""

from __future__ import print_function

import argparse
from datetime import datetime
import os
import sys
import time
import scipy.io as sio
from glob import glob

import tensorflow as tf
from time import perf_counter
import numpy as np
import pdb

from parse_opt import get_arguments
from deeplab_resnet import HyperColumn_Deeplabv2, read_data_list

IMG_MEAN = np.array((104.00698793,116.66876762,122.67891434), dtype=np.float32)


#######################################################
'''
Helper functions
'''

def load_dir_structs(dataset_path):
	# Get list of subdirs
# 	types = ('*.jpg', '*.png')	# jpg is not supported yet by read_img()
	types = ('*.png',)
	
	curflist= []
	for files in types:
		curflist.extend(glob(os.path.join(dataset_path, files)))
	return curflist


def read_img(t_imgfname, input_size, img_mean): # optional pre-processing arguments
	"""Read one image and its corresponding mask with optional pre-processing.
	
	Args:
	  input_queue: tf queue with paths to the image and its mask.
	  input_size: a tuple with (height, width) values.
				  If not given, return images of original size.
	  random_scale: whether to randomly scale the images prior
					to random crop.
	  random_mirror: whether to randomly mirror the images prior
					to random crop.
	  ignore_label: index of label to ignore during the training.
	  img_mean: vector of mean colour values.
	  
	Returns:
	  Two tensors: the decoded image and its mask.
	"""

	img_contents = tf.io.read_file(t_imgfname)
	
# 	img = tf.image.decode_image(img_contents, channels=3)
	img = tf.image.decode_png(img_contents, channels=3)
	img_r, img_g, img_b = tf.split(axis=2, num_or_size_splits=3, value=img)
	img = tf.cast(tf.concat(axis=2, values=[img_b, img_g, img_r]), dtype=tf.float32)
	# Extract mean.
	img -= img_mean
	
	if input_size is not None:
		h, w = input_size

		# Randomly scale the images and labels.
		newshape = tf.squeeze(tf.stack([h, w]), axis=[1])
		img2 = tf.image.resize(img, newshape)
	else:
		img2 = tf.image.resize(img, tf.shape(input=img)[0:2,]*2)
		
	return img2, img



#######################################################
'''
Main function
'''
if __name__ == "__main__":
	args = get_arguments()

	# Set up tf session and initialize variables. 
	config = tf.compat.v1.ConfigProto()
	config.gpu_options.allow_growth = True
	with tf.compat.v1.Session(config=config) as sess:
		model = HyperColumn_Deeplabv2(sess, args)

		# Load variables if the checkpoint is provided.
		model.load(args.snapshot_dir)
		
		local_imgflist = load_dir_structs(args.data_dir)
		save_folder = args.feat_dir
		if not os.path.exists(save_folder):
			os.mkdir(save_folder)

		for i in range(len(local_imgflist)):
			if os.path.splitext(local_imgflist[i])[1] == '':
				continue

			print('{} Processing {}'.format(i, local_imgflist[i]))
			padsize = 50
			# the following read_img() calls could lead to a memory leakage-like issue or at least very slow. (need to be fixed later)
			_, ori_img = read_img(local_imgflist[i], input_size = None, img_mean = IMG_MEAN)
			start = perf_counter()
			pad_img = tf.pad(tensor=ori_img, paddings=[[padsize,padsize], [padsize,padsize], [0,0]], mode='REFLECT')
			cur_embed = model.test(pad_img.eval())
			cur_embed = np.squeeze(cur_embed)
			end = perf_counter()
			curfname = os.path.split(os.path.splitext(local_imgflist[i])[0])[1]
			cur_svpath = os.path.join(save_folder, curfname + '.mat')
			print(cur_svpath)
			print(f"took {end - start} seconds to generate features")
			sio.savemat(cur_svpath, {'embedmap': cur_embed[padsize:(cur_embed.shape[0]-padsize),padsize:(cur_embed.shape[1]-padsize),:]})
		

			






