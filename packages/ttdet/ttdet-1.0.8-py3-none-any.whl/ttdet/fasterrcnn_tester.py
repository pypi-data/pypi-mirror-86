from mmdet.apis import init_detector, inference_detector, show_result
import mmcv
import numpy as np
import pycocotools.mask as maskUtils
from time import time
import configparser
import cv2
from ttcv.import_basic_utils import *
from ttcv.basic.basic_objects import BasDetectObj

class FasterRCNNDetector():
    def get_model(self, config_file, checkpoint_file):
        self.model = init_detector(config_file, checkpoint_file, device='cuda:0')

    def predict_array(self, im, need_rot=False, test_shape=None, classes=None, thresh=None):
        h,w = im.shape[:2]
        if need_rot: im_rot =  cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)#np.rot90(anArray, k=-1)           # 90 rot
        else: im_rot = im

        need_reshape = (test_shape!=(w,h))
        if need_reshape:
            h1, w1 = im_rot.shape[:2]
            im_scale = cv2.resize(im_rot, test_shape, interpolation=cv2.INTER_CUBIC)
            h2, w2 = im_scale.shape[:2]
            fx, fy = w1/w2, h1/h2       # restore ratios
        else: im_scale = im_rot

        boxes_list=inference_detector(self.model, im_scale)

        boxes, scores, bclasses = [], [], []
        for j, _boxes in enumerate(boxes_list):
            if len(_boxes) == 0: continue
            _scores = _boxes[:, -1].reshape((-1,1))
            if thresh is not None:
                inds = _scores.flatten() > thresh
                _boxes = _boxes[inds, :4]
                _scores = _scores[inds, :]
            num_box = len(_boxes)
            if num_box==0: continue
            boxes.append(_boxes)
            scores.append(_scores)
            if classes is None: bclasses += [str(j)]*num_box
            else: bclasses +=[classes[j]]*num_box

        if len(boxes) == 0: return None
        boxes, scores = np.vstack(boxes), np.vstack(scores)


        if need_reshape: boxes[:,[0,2]], boxes[:,[1,3]] = boxes[:,[0,2]]*fx, boxes[:,[1,3]]*fy

        if need_rot:
            boxes = boxes[:, [1,2,3,0]]
            boxes[:, [1, 3]] = h - boxes[:, [1, 3]]

        return (boxes.astype('int'), scores, bclasses)

    def show_boxes(self, im , boxes, labels=None, colors=None, line_thick=2, text_scale=1.2, text_thick=2):
        out = np.copy(im)
        if len(boxes)==0: return  im
        for j,box in enumerate(boxes.astype('int')):
            left, top, right, bottom = box
            if colors is None: color = (0,255,0)
            else: color = colors[j]
            cv2.rectangle(out, (left, top), (right, bottom), color, line_thick)
            if labels is not None:
                cv2.putText(out, labels[j], (left, top), cv2.FONT_HERSHEY_COMPLEX, text_scale, color, text_thick)

        return out











