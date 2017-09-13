from image.frame import Frame
from image.box import Box
from image.object import Object
from data_loading.samplers.sampler import Sampler
from data_loading.sample import Sample
from image.affine import Affine
from image.image_utils import PIL_to_cudnn_np, scale_np_img
from excepts.general_exceptions import NoFramesException
import numpy as np
import random
import torch

class CropSampler(Sampler):

    def __init__(self,source,params):
        Sampler.__init__(self,source)
        self.seed = params.get('seed',123)
        self.crop_size = params['crop_size']
        self.obj_types = params['obj_types']
        random.seed(self.seed)

        self.frame_ids = []
        #index all the frames that have at least one item we want
        # TODO turn this into a re-usable filter module
        for i,frame in enumerate(self.source):
            crop_objs = filter(lambda x: x.obj_type in self.obj_types,frame.get_objects())
            if(len(crop_objs)>0):
                self.frame_ids.append(i)

        print 'The source has {0} items'.format(len(self.source))
        if len(self.frame_ids)==0:
            raise NoFramesException('No Valid Frames Found!')

        print '{0} frames found'.format(len(self.frame_ids))

    def next(self):
        # just grab the next random frame
        frame = self.source[random.choice(self.frame_ids)]

        # data = np.array((len(crop_objs),self.crop_size[0],self.crop_size[1],3),dtype=float,order='C')
        # targets = np.array((len(crop_objs),self.crop_size[0],self.crop_size[1],3),dtype=float,order='C')
        frame_shape = frame.get_numpy_image().shape
        data = None

        frame_image = frame.get_image()
        crop_objs = filter(lambda x: x.obj_type in self.obj_types,frame.get_objects())
        print 'Num crop objs in sample: {0}'.format(len(crop_objs))

        for crop in crop_objs:
            # crop and resize
            crop_image = frame_image.crop(crop.box.to_single_array())
            resized_image = crop_image.resize(self.crop_size)

            np_img = scale_np_img(PIL_to_cudnn_np(resized_image),[0,255],[0,1])
            # TODO as scale target boxes
            if data is not None:
                # stack crop on top of tensor along first aWWxis
                reshaped_img = np_img.reshape([1]+list(np_img.shape))
                data = np.concatenate((data,reshaped_img),axis=0)
            else:
                # new data
                data = np_img
                data = data.reshape([1]+list(data.shape))

        sample = Sample(torch.Tensor(data.astype(float)),torch.Tensor())

        return sample