#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 16:46
# @Author  : caozhiye

import tensorflow as tf
import numpy as np
from PIL import Image
import os
#import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 屏蔽tensorflow运行时CPU指令集警告
CAPTCHA_LEN = 4

# projname='yaoex_app_auto_android'
# root_dir=os.path.abspath(os.path.dirname(__file__)).split(projname)[0]+projname+os.sep
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR: ',BASE_DIR)


def predict_captcha(color_type, captcha_name):
    """
    根据验证码图片预测验证码
    @param color_type: 验证码颜色类型：colorful-彩色；   blackwhite-黑白；
    @param captcha_name: 验证码文件名
    @return: 验证码字符串
    """
    if color_type not in ['colorful','blackwhite']:
        raise Exception('验证码类型参数值应该是以下值：：colorful（彩色）；   blackwhite（黑白）')
    #image_dir=BASE_DIR+'file'+os.sep+'captcha'+os.sep+'images'+os.sep
    image_path=os.path.join(BASE_DIR,'localplugins','captcha', 'images',captcha_name)
    if os.path.exists(image_path)==False:
        raise Exception('未找到文件：',image_path)
    #model_dir=BASE_DIR+'file'+os.sep+'captcha'+os.sep+'models'+os.sep+color_type+os.sep
    model_dir=os.path.join(BASE_DIR,'localplugins','captcha', 'models',color_type)
    if color_type=='colorful':
        model_file_name = "crack_captcha.model.meta"
    elif color_type=='blackwhite':
        model_file_name = "crack_captcha.model-2600.meta"
    model_path=os.path.join(BASE_DIR,'localplugins','captcha', 'models',color_type,model_file_name)
    # 加载graph
    saver = tf.train.import_meta_graph(model_path)
    graph = tf.get_default_graph()

    # 从graph取得tensor，他们的name是在构建graph时定义的
    input_holder = graph.get_tensor_by_name("data-input:0")
    keep_prob_holder = graph.get_tensor_by_name("keep-prob:0")
    predict_max_idx = graph.get_tensor_by_name("predict_max_idx:0")

    #  预测验证码
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint(model_dir))
        img = Image.open(image_path)
        # 转为灰度图
        img = img.convert("L")
        image_array = np.array(img)
        image_data = image_array.flatten() / 255
        
        predict = sess.run(predict_max_idx, feed_dict={input_holder: [image_data], keep_prob_holder: 1.0})
        
        predict_value = np.squeeze(predict).tolist()  # 预测验证码并将结果numpy.ndarray 转化成list

        #print(predict_value)  # [3, 4, 2, 5]，整数为元素的列表
        # 将列表元素转换成字符串拼接输出
        captcha_text = ""
        for item in predict_value:
            #text = str(item)            
            text=str(hex(item))[-1]     #药网验证码含有字母，需要10进制转换为16进制
            captcha_text = captcha_text + text

        print("%s 识别出的验证码为:%s" % (image_path, captcha_text))
        return captcha_text

if __name__ == '__main__':
    predict_captcha('blackwhite','captcha_b2bapp_findpassword.png')
    #predict_captcha('colorful','captcha_b2bpc.png')
