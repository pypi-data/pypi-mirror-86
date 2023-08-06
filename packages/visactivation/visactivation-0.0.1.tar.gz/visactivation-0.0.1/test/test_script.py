import numpy as np
import cv2
import argparse
import os
from PIL import Image
from function import *
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--tensor", default='test1.png', type=str)
	parser.add_argument("--image", default='test1.jpg', type=str)
	parser.add_argument("--output", default='output1', type=str)
	args = parser.parse_args()
	if 'png' in args.tensor:
		tensor = np.array(Image.open(args.tensor))
	elif 'npy' in args.tensor:
		tensor = np.load(args.tensor)
		tensor[0,:,:] = 0
	else:
		raise ValueError('Can\'t load %s'%args.tensor)
	image = cv2.imread(args.image)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	print('tensor.shape')
	print(tensor.shape)
	print('image.shape')
	print(image.shape)

	input_type_dict = {2:'HW', 3:'CHW', 4:'NCHW'}
	act_type_list = ['sum', 'max', 'mean', 'none']
	norm_type_list = ['all', 'relu', 'none']
	for tensor_dim in [2,3,4]:
		for image_dim in [3,4]:
			print('tensor_dim:%d\timage_dim:%d'%(tensor_dim, image_dim))
			test_tensor = tensor
			test_image = image
			output_file = args.output+'.png'
			output_image_file = args.output+'_image.png'
			if os.path.exists(output_file):
				os.remove(output_file)
			if os.path.exists(output_image_file):
				os.remove(output_image_file)

			for i in range(tensor.ndim, tensor_dim):
				test_tensor = np.expand_dims(test_tensor, axis=0)
			for i in range(image.ndim, image_dim):
				test_image = np.expand_dims(test_image, axis=0)
				
			tensor_color = Label2Color(test_tensor, colormap='random')
			tensor_color = cv2.cvtColor(tensor_color[0], cv2.COLOR_RGB2BGR)	
			cv2.imwrite(output_file, tensor_color)

			tensor_image_color = Label2Color(test_tensor, image=test_image, image_weight=0.3, colormap='random')
			tensor_image_color = cv2.cvtColor(tensor_image_color[0], cv2.COLOR_RGB2BGR)	
			cv2.imwrite(output_image_file, tensor_image_color)

	#		input('write finished, wait for continue...')
#	for tensor_dim in [4, 3]:
#		for image_dim in [3,4]:
#			for act_type in act_type_list:
#				for norm_type in norm_type_list:
#					print('tensor_dim:%d\timage_dim:%d\tact_type:%s\tnorm_type:%s'%(tensor_dim, image_dim, act_type, norm_type))
#					test_tensor = tensor
#					test_image = image
#					output_file = args.output+'.png'
#					output_image_file = args.output+'_image.png'
#					if os.path.exists(output_file):
#						os.remove(output_file)
#					if os.path.exists(output_image_file):
#						os.remove(output_image_file)
#		
#					for i in range(tensor.ndim, tensor_dim):
#						test_tensor = np.expand_dims(test_tensor, axis=0)
#					for i in range(image.ndim, image_dim):
#						test_image = np.expand_dims(test_image, axis=0)
#						
#					#tensor_color = Tensor2Color(test_tensor, input_type=input_type_dict[tensor_dim], colormap='random', act_type=act_type, norm_type=norm_type)
#					#tensor_color = Tensor2Color(test_tensor, colormap='random', act_type=act_type, norm_type=norm_type)
#					tensor_color = Prob2Color(test_tensor, input_type=input_type_dict[tensor_dim], colormap='random', act_type=act_type)
#					if tensor_color.shape[1] == 1:
#						tensor_color = cv2.cvtColor(tensor_color[0,0], cv2.COLOR_RGB2BGR)	
#						cv2.imwrite(output_file, tensor_color)
#		
#					#tensor_image_color = Tensor2Color(test_tensor, input_type=input_type_dict[tensor_dim], image=test_image, image_weight=0.3, colormap='random', act_type=act_type, norm_type=norm_type)
#					#tensor_image_color = Tensor2Color(test_tensor, image=test_image, image_weight=0.3, colormap='random', act_type=act_type, norm_type=norm_type)
#					tensor_image_color = Prob2Color(test_tensor, input_type=input_type_dict[tensor_dim], image=test_image, image_weight=0.3, colormap='random', act_type=act_type)
#					if tensor_image_color.shape[1] == 1:
#						tensor_image_color = cv2.cvtColor(tensor_image_color[0,0], cv2.COLOR_RGB2BGR)	
#						cv2.imwrite(output_image_file, tensor_image_color)
#					print('write finished')
#
#					#input('wait for continue...')
#		
		
