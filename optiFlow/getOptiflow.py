# -*- coding: utf-8 -*-
# @Time     : 2018/12/10 16:55
# @Author   : vickylzy
# original code:"https://docs.opencv.org/4.0.0-beta/d7/d8b/tutorial_py_lucas_kanade.html"

import numpy as np
import cv2 as cv
import os

target_name = '../video/fin.flv'
if not os.path.exists(target_name):
    print('file not exists!')
cap = cv.VideoCapture(target_name)

# 测试视频读取        # frame.shape  (480 580+-)
# ret, frame = cap.read()
# if frame is not None:
#     cv.namedWindow('pool', cv.WINDOW_NORMAL)
#     cv.imshow('pool', frame)
#     cv.waitKey()
#     1==1
# 角点参数
feature_param = dict(maxCorners=100,
                     qualityLevel=0.3,
                     minDistance=7,
                     blockSize=7,
                     mask=None)
# LK法参数
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors ---why???
color = np.random.randint(0, 255, (100, 3))
# 初始帧寻找优秀角点
ret, ori_frame = cap.read()
ori_gray = cv.cvtColor(ori_frame, cv.COLOR_BGR2GRAY)
ori_corners = cv.goodFeaturesToTrack(ori_gray, **feature_param)

# 画布
mask = np.zeros_like(ori_frame)  # 函数返回一个等大小0矩阵
frame_Num = 1
while True:
    # 获取当前帧
    ret, curr_frame = cap.read()
    curr_gray = cv.cvtColor(curr_frame, cv.COLOR_BGR2GRAY)
    # curr_corner = cv.goodFeaturesToTrack(curr_gray,**feature_param)   #和其特征角点
    # LK光流
    curr_corners, status, err = cv.calcOpticalFlowPyrLK(ori_gray, curr_gray, ori_corners, None, **lk_params)

    # 选择匹配上点
    match_ori = ori_corners[status]
    match_curr = curr_corners[status]

    # 展示路径
    for i, (new_cor, ori_cor) in enumerate(zip(match_curr, match_ori)):
        a, b = new_cor.ravel()  # 返回一维数据，new_cor内嵌套维度过高
        c, d = ori_cor.ravel()
        mask = cv.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        frame = cv.circle(curr_frame, (a, b), 5, color[i].tolist(), -1)
    img = cv.add(curr_frame, mask)
    cv.imshow('frame', img)
    k = cv.waitKey() & 0xff
    # if k == 27:
    #     break
    # Now update the previous frame and  previous points
    frame_Num = frame_Num + 1
    if frame_Num == 134:
        break
    old_gray = curr_gray.copy()
    p0 = match_curr.reshape(-1, 1, 2)
cv.destroyAllWindows()
cap.release()