import tempfile
import os
import pickle
import random

import numpy as np

from ..data_providers.base_provider import ImagesDataSet, DataProvider
from ..data_providers.downloader import download_data_url


def augment_image(image, pad):
	"""Perform zero padding, randomly crop image to original size,
	maybe mirror horizontally"""
	init_shape = image.shape
	new_shape = [init_shape[0] + pad * 2,
				 init_shape[1] + pad * 2,
				 init_shape[2]]
	zeros_padded = np.zeros(new_shape)
	zeros_padded[pad:init_shape[0] + pad, pad:init_shape[1] + pad, :] = image
	# randomly crop to original size
	init_x = np.random.randint(0, pad * 2)
	init_y = np.random.randint(0, pad * 2)
	cropped = zeros_padded[
			  init_x: init_x + init_shape[0],
			  init_y: init_y + init_shape[1],
			  :]
	flip = random.getrandbits(1)
	if flip:
		cropped = cropped[:, ::-1, :]
	return cropped


def augment_all_images(initial_images, pad=4):
	new_images = np.zeros(initial_images.shape)
	for i in range(initial_images.shape[0]):
		new_images[i] = augment_image(initial_images[i], pad)
	return new_images


class CifarDataSet(ImagesDataSet):
	def __init__(self, images, labels, n_classes, shuffle, normalization, augmentation, meanstd):
		"""
		Args:
			images: 4D numpy array
			labels: 2D or 1D numpy array
			n_classes: `int`, number of cifar classes - 10 or 100
			shuffle: `str` or None
				None: no any shuffling
				once_prior_train: shuffle train data only once prior train
				every_epoch: shuffle train data prior every epoch
			normalization: `str` or None
				None: no any normalization
				divide_255: divide all pixels by 255
				divide_256: divide all pixels by 256
				by_channels: substract mean of every chanel and divide each
					chanel data by it's standard deviation
			augmentation: `bool`
		"""
		if shuffle is None:
			self.shuffle_every_epoch = False
		elif shuffle == 'once_prior_train':
			self.shuffle_every_epoch = False
			images, labels = self.shuffle_images_and_labels(images, labels)
		elif shuffle == 'every_epoch':
			self.shuffle_every_epoch = True
		else:
			raise Exception('Unknown type of shuffling')
		self._batch_counter, self.epoch_images, self.epoch_labels = 0, None, None
		
		self.images = images
		self.labels = labels
		self.n_classes = n_classes
		self.augmentation = augmentation
		self.normalization = normalization
		self.meanstd = meanstd
		self.images = self.normalize_images(images, self.normalization, self.meanstd)
		self.start_new_epoch()
	
	def start_new_epoch(self):
		self._batch_counter = 0
		if self.shuffle_every_epoch:
			images, labels = self.shuffle_images_and_labels(
				self.images, self.labels)
		else:
			images, labels = self.images, self.labels
		if self.augmentation:
			images = augment_all_images(images, pad=4)
		self.epoch_images = images
		self.epoch_labels = labels
	
	@property
	def num_examples(self):
		return self.labels.shape[0]
	
	def next_batch(self, batch_size):
		start = self._batch_counter * batch_size
		end = (self._batch_counter + 1) * batch_size
		self._batch_counter += 1
		images_slice = self.epoch_images[start: end]
		labels_slice = self.epoch_labels[start: end]
		if images_slice.shape[0] != batch_size:
			self.start_new_epoch()
			return self.next_batch(batch_size)
		else:
			return images_slice, labels_slice


class CifarDataProvider(DataProvider):
	"""Abstract class for cifar readers"""
	def __init__(self, save_path=None, validation_size=None, shuffle=None, normalization=None,
				 one_hot=True, **kwargs):
		"""
		Args:
			save_path: `str`
			validation_set: `bool`.
			validation_split: `float` or None
				float: chunk of `train set` will be marked as `validation set`.
				None: if 'validation set' == True, `validation set` will be
					copy of `test set`
			shuffle: `str` or None
				None: no any shuffling
				once_prior_train: shuffle train data only once prior train
				every_epoch: shuffle train data prior every epoch
			normalization: `str` or None
				None: no any normalization
				divide_255: divide all pixels by 255
				divide_256: divide all pixels by 256
				by_channels: substract mean of every chanel and divide each
					chanel data by it's standard deviation
			one_hot: `bool`, return laels one hot encoded
		"""
		self._save_path = save_path
		self.one_hot = one_hot
		download_data_url(self.data_url, self.save_path)
		train_fnames, test_fnames = self.get_filenames(self.save_path)
		
		# add train and validations datasets
		images, labels = self.read_cifar(train_fnames)
		train_meanstd = ImagesDataSet.measure_mean_and_std(images)
		if validation_size is not None:
			np.random.seed(DataProvider._SEED)
			rand_indexes = np.random.permutation(images.shape[0])
			valid_indexes = rand_indexes[:validation_size]
			train_indexes = rand_indexes[validation_size:]
			self.train = CifarDataSet(
				images=images[train_indexes], labels=labels[train_indexes],
				n_classes=self.n_classes, shuffle=shuffle,
				normalization=normalization,
				augmentation=self.data_augmentation, meanstd=train_meanstd)
			self.validation = CifarDataSet(
				images=images[valid_indexes], labels=labels[valid_indexes],
				n_classes=self.n_classes, shuffle=None,
				normalization=normalization,
				augmentation=False, meanstd=train_meanstd)
		else:
			self.train = CifarDataSet(
				images=images, labels=labels,
				n_classes=self.n_classes, shuffle=shuffle,
				normalization=normalization,
				augmentation=self.data_augmentation, meanstd=train_meanstd)
		
		# add test set
		images, labels = self.read_cifar(test_fnames)
		self.test = CifarDataSet(
			images=images, labels=labels,
			shuffle=None, n_classes=self.n_classes,
			normalization=normalization,
			augmentation=False, meanstd=train_meanstd)
		
		if validation_size is None:
			self.validation = self.test
	
	@property
	def save_path(self):
		if self._save_path is None:
			self._save_path = os.path.join(
				tempfile.gettempdir(), 'cifar%d' % self.n_classes)
		return self._save_path
	
	@property
	def data_url(self):
		"""Return url for downloaded data depends on cifar class"""
		data_url = ('http://www.cs.toronto.edu/'
					'~kriz/cifar-%d-python.tar.gz' % self.n_classes)
		return data_url
	
	@property
	def data_shape(self):
		return 32, 32, 3
	
	@property
	def n_classes(self):
		return self._n_classes
	
	def get_filenames(self, save_path):
		"""Return two lists of train and test filenames for dataset"""
		raise NotImplementedError
	
	def read_cifar(self, filenames):
		if self.n_classes == 10:
			labels_key = b'labels'
		elif self.n_classes == 100:
			labels_key = b'fine_labels'
		
		images_res = []
		labels_res = []
		for fname in filenames:
			with open(fname, 'rb') as f:
				images_and_labels = pickle.load(f, encoding='bytes')
			images = images_and_labels[b'data']
			images = images.reshape(-1, 3, 32, 32)
			images = images.swapaxes(1, 3).swapaxes(1, 2)
			images_res.append(images)
			labels_res.append(images_and_labels[labels_key])
		images_res = np.vstack(images_res)
		labels_res = np.hstack(labels_res)
		if self.one_hot:
			labels_res = self.labels_to_one_hot(labels_res)
		return images_res, labels_res


class Cifar10DataProvider(CifarDataProvider):
	_n_classes = 10
	data_augmentation = False
	
	def get_filenames(self, save_path):
		sub_save_path = os.path.join(save_path, 'cifar-10-batches-py')
		train_filenames = [
			os.path.join(
				sub_save_path,
				'data_batch_%d' % i) for i in range(1, 6)]
		test_filenames = [os.path.join(sub_save_path, 'test_batch')]
		return train_filenames, test_filenames


class Cifar100DataProvider(CifarDataProvider):
	_n_classes = 100
	data_augmentation = False
	
	def get_filenames(self, save_path):
		sub_save_path = os.path.join(save_path, 'cifar-100-python')
		train_filenames = [os.path.join(sub_save_path, 'train')]
		test_filenames = [os.path.join(sub_save_path, 'test')]
		return train_filenames, test_filenames


class Cifar10AugmentedDataProvider(Cifar10DataProvider):
	_n_classes = 10
	data_augmentation = True


class Cifar100AugmentedDataProvider(Cifar100DataProvider):
	_n_classes = 100
	data_augmentation = True

