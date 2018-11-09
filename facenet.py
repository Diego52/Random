from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from subprocess import Popen, PIPE
import tensorflow as tf
import numpy as np
from scipy import misc
from sklearn.model_selection import KFold
from scipy import interpolate
from tensorflow.python.training import training
import random
import re
from tensorflow.python.platform import gfile
import math
from sklearn.svm import SVC
import pickle
from six import iteritems
from utils import input_data

class ImageClass():
    "Stores the paths to images for a given class"
    def __init__(self, name, image_paths):
        self.name = name
        self.image_paths = image_paths
  
    def __str__(self):
        return self.name + ', ' + str(len(self.image_paths)) + ' images'
  
    def __len__(self):
        return len(self.image_paths)

class Facenet:
    def __init__(self, config):
        self.model = config['model']
        self.image_size = config['image_size']
        self.seed = config['seed']
        self.graph = None
        self.images_placeholder = None
        self.embeddings = None
        self.phase_train_placeholder = None
        self.sess = None
        self.embedding_size = None

    def train_model(self, group_folder):
        batch_size = 1000
        image_size = 160
        svm_name = input_data.name_now()
        classifier_filename = group_folder + 'svm/' + svm_name + '.pkl'
        csv_filename = group_folder + 'info/' + svm_name + '.csv'
        in_folder = group_folder + 'images/faces/'
        dataset = self.get_dataset(in_folder)
        paths, labels = self.get_image_paths_and_labels(dataset)
        
        print('Number of classes: %d' % len(dataset))
        print('Number of images: %d' % len(paths))
        
        
        # Run forward pass to calculate embeddings
        print('Calculating features for images')
        nrof_images = len(paths)
        nrof_batches_per_epoch = int(math.ceil(1.0*nrof_images / batch_size))
        emb_array = np.zeros((nrof_images, self.embedding_size))
        for i in range(nrof_batches_per_epoch):
            start_index = i*batch_size
            end_index = min((i+1)*batch_size, nrof_images)
            paths_batch = paths[start_index:end_index]
            images = self.load_data(paths_batch, False, False, image_size)
            emb_array[start_index:end_index,:] = self.predict(images, False)
        
        classifier_filename_exp = os.path.expanduser(classifier_filename)

        # Train classifier
        print('Training classifier')
        model = SVC(kernel= str(u'rbf'),probability=True)
        model.fit(emb_array, labels)
    
        # Create a list of class names
        class_names = [ cls.name.replace('_', ' ') for cls in dataset]

        if not os.path.exists(group_folder + 'info/'):
            os.mkdir(group_folder + 'info/')
        
        with open(csv_filename, 'w') as csv_file:
            csv_file.write(','.join(class_names))

        # Saving classifier model
        with open(classifier_filename_exp, 'wb') as outfile:
            pickle.dump((model, class_names), outfile, protocol=2)
        print('Saved classifier model to file "%s"' % classifier_filename_exp)

    def load_data(self, image_paths, do_random_crop, do_random_flip, image_size, do_prewhiten=True):
        nrof_samples = len(image_paths)
        images = np.zeros((nrof_samples, image_size, image_size, 3))
        for i in range(nrof_samples):
            img = misc.imread(image_paths[i])
            if img.ndim == 2:
                img = self.to_rgb(img)
            if do_prewhiten:
                img = self.prewhiten(img)
            img = self.crop(img, do_random_crop, image_size)
            img = self.flip(img, do_random_flip)
            images[i,:,:,:] = img
        return images
    
    def to_rgb(self, img):
        w, h = img.shape
        ret = np.empty((w, h, 3), dtype=np.uint8)
        ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
        return ret

    def get_image_paths_and_labels(self, dataset):
        image_paths_flat = []
        labels_flat = []
        for i in range(len(dataset)):
            image_paths_flat += dataset[i].image_paths
            labels_flat += [i] * len(dataset[i].image_paths)
        return image_paths_flat, labels_flat

    def get_dataset(self, path, has_class_directories=True):
        dataset = []
        path_exp = os.path.expanduser(path)
        classes = [path for path in os.listdir(path_exp) \
                        if os.path.isdir(os.path.join(path_exp, path))]
        classes.sort()
        nrof_classes = len(classes)
        for i in range(nrof_classes):
            class_name = classes[i]
            facedir = os.path.join(path_exp, class_name)
            print(facedir)
            image_paths = self.get_image_paths(facedir)
            dataset.append(ImageClass(class_name, image_paths))
        return dataset
    
    def get_image_paths(self, facedir):
        image_paths = []
        if os.path.isdir(facedir):
            images = os.listdir(facedir)
            image_paths = [os.path.join(facedir,img) for img in images]
        return image_paths

    def load_model(self):
    # Check if the model is a model directory (containing a metagraph and a checkpoint file)
    #  or if it is a protobuf file with a frozen graph
        model_exp = os.path.expanduser(self.model)
        if (os.path.isfile(model_exp)):
            print('Model filename: %s' % model_exp)
            with gfile.FastGFile(model_exp,'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
            with tf.Graph().as_default() as graph:
                tf.import_graph_def(graph_def, name='prefix')
            self.graph = graph
            self.images_placeholder = self.graph.get_tensor_by_name('prefix/input:0')
            self.embeddings = self.graph.get_tensor_by_name('prefix/embeddings:0')
            self.phase_train_placeholder = self.graph.get_tensor_by_name('prefix/phase_train:0')
            self.embedding_size = self.embeddings.get_shape()[1]
            self.sess = tf.Session(graph=self.graph)


    def one_image_to_emb(self, img, do_random_crop, do_random_flip, image_size, do_prewhiten=True):
        if do_prewhiten:
            img = self.prewhiten(img)
        img = self.crop(img, do_random_crop, image_size)
        img = self.crop(img, do_random_crop, image_size)
        img = self.flip(img, do_random_flip)
        img = np.expand_dims(img, axis=0)
        return img
    
    def flip(self, image, random_flip):
        if random_flip and np.random.choice([True, False]):
            image = np.fliplr(image)
        return image

    def crop(self, image, random_crop, image_size):
        if image.shape[1]>image_size:
            sz1 = int(image.shape[1]//2)
            sz2 = int(image_size//2)
            if random_crop:
                diff = sz1-sz2
                (h, v) = (np.random.randint(-diff, diff+1), np.random.randint(-diff, diff+1))
            else:
                (h, v) = (0,0)
            image = image[(sz1-sz2+v):(sz1+sz2+v),(sz1-sz2+h):(sz1+sz2+h),:]
        return image

    def prewhiten(self, x):
        mean = np.mean(x)
        std = np.std(x)
        std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
        y = np.multiply(np.subtract(x, mean), 1/std_adj)
        return y
    
    def predict(self, image, phase):
        feed_dict = { self.images_placeholder: image, self.phase_train_placeholder:phase }
        emb_array = self.sess.run(self.embeddings, feed_dict=feed_dict)
        return emb_array