# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 17:09:47 2020

@author: Desktop
"""
import tensorflow as tf

class TFRecordManager():
    
    ImageSize = 96
    
    def bytes_feature(self,values):
      return tf.train.Feature(bytes_list=tf.train.BytesList(value=[values]))
    
    def int64_feature(self,values):
      if not isinstance(values, (tuple, list)):
        values = [values]
      return tf.train.Feature(int64_list=tf.train.Int64List(value=values))
    
    def read_imagebytes(self,imagefile):
        file = open(imagefile,'rb')
        bytes = file.read()
        return bytes
    
    def writeTFRecord(self, labelNumber, imagepath):
        image_data = self.read_imagebytes(imagepath)
        tf_example = tf.train.Example(features=tf.train.Features(           
            feature={
                'image/encoded': self.bytes_feature(image_data), 
                'image/format': self.bytes_feature(b'jpg'), 
                'image/class/label': self.int64_feature(labelNumber), 
                'image/height': self.int64_feature(self.ImageSize), 
                'image/width': self.int64_feature(self.ImageSize),
    	}))
        
        writer = tf.compat.v1.python_io.TFRecordWriter('output_filename.tfrecord')
        writer.write(tf_example.SerializeToString())

    
    	
    
    