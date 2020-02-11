import cv2
import numpy as np
#from os import listdir
#from os.path import isfile, join
from math import sqrt
import os
import sys
import time
from matplotlib import pyplot as plt


import json

#Code has been obtained from: https://github.com/dongb5/Retinex
def singleScaleRetinex(img, sigma):
    retinex = np.log10(img) - np.log10(cv2.GaussianBlur(img, (0, 0), sigma))
    return retinex

def colorRestoration(img, alpha, beta):
    img_sum = np.sum(img, axis=2, keepdims=True)
    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))
    return color_restoration

def multiScaleRetinex(img, sigma_list):
    retinex = np.zeros_like(img)
    for sigma in sigma_list:
        retinex += singleScaleRetinex(img, sigma)
    retinex = retinex / len(sigma_list)
    return retinex

def simplestColorBalance(img, low_clip, high_clip):
    total = img.shape[0] * img.shape[1]
    for i in range(img.shape[2]):
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        for u, c in zip(unique, counts):
            if float(current) / total < low_clip:
                low_val = u
            if float(current) / total < high_clip:
                high_val = u
            current += c
        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)
    return img

def MSRCR(img, sigma_list, G, b, alpha, beta, low_clip, high_clip):
    img = np.float64(img) + 1.0
    img_retinex = multiScaleRetinex(img, sigma_list)
    img_color = colorRestoration(img, alpha, beta)
    img_msrcr = G * (img_retinex * img_color + b)

    for i in range(img_msrcr.shape[2]):
        img_msrcr[:, :, i] = (img_msrcr[:, :, i] - np.min(img_msrcr[:, :, i])) / \
                             (np.max(img_msrcr[:, :, i]) - np.min(img_msrcr[:, :, i])) * \
                             255
    img_msrcr = np.uint8(np.minimum(np.maximum(img_msrcr, 0), 255))
    img_msrcr = simplestColorBalance(img_msrcr, low_clip, high_clip)
    return img_msrcr

def brightening(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    x0 = len(hsv)
    y0 = len(hsv[0]) / 2
    for x in range(0, x0):
        for y in range(0, len(hsv[0])):
            value = 0.00025 * sqrt(pow((x - x0), 2) + pow((y - y0), 2))
            hsv[x, y] += round(value)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def clahe(bgr):
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(50, 50))

    lab_planes[0] = clahe.apply(lab_planes[0])

    lab = cv2.merge(lab_planes)

    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr

def ih(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    img_ih = plt.hist(img.ravel(), 256, [0,256])
    return img_ih

data_path = "Image/data"
result_path = "Image/result_process"
result_ih_path = "result_ih"
result_sobel_path = "result_sobel"
result_sobel_ih_path = "result_sobel_ih"


img_list = os.listdir(data_path)
if len(img_list) == 0:
    print('Data directory is empty.')
    exit()

with open('config_processing.json', 'r') as f:
    config = json.load(f)

for img_name in img_list:
    img = cv2.imread(os.path.join(data_path, img_name))
    print(time.strftime("%H:%M:%S", time.localtime()), "Processing image: ", img_name)

    body, ext = os.path.splitext(img_name)
     
    #0 write original image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[0/15] Original")
    name_0 = body + ".00.jpg"
    cv2.imwrite(os.path.join(result_path, name_0), img)
    

    #1 B write Brightening image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[1/15] Brightening")
    img_1 = brightening(img)
    name_1 = body + ".01.jpg"
    cv2.imwrite(os.path.join(result_path, name_1), img_1)


    #2 R write Retinex image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[2/15] Retinex")
    img_2 = MSRCR(img,config['sigma_list'],config['G'],config['b'],config['alpha'],config['beta'],config['low_clip'],config['high_clip'])
    name_2 = body + ".02.jpg"
    cv2.imwrite(os.path.join(result_path, name_2), img_2)


    #3 C write CLAHE image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[3/15] CLAHE")
    img_3 = clahe(img)
    name_3 = body + ".03.jpg"
    cv2.imwrite(os.path.join(result_path, name_3), img_3)


    #4 B+R write Brightening + Retinex image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[4/15] Brightening + Retinex")
    img_4 = MSRCR(img_1,config['sigma_list'],config['G'],config['b'],config['alpha'],config['beta'],config['low_clip'],config['high_clip'])
    name_4 = body + ".04.jpg"
    cv2.imwrite(os.path.join(result_path, name_4), img_4)


    #5 R+B write Retinex + Brightening image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[5/15] Retinex + Brightening")
    img_5 = brightening(img_2)
    name_5 = body + ".05.jpg"
    cv2.imwrite(os.path.join(result_path, name_5), img_5)


    #6 B+C write Brightening + CLAHE image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[6/15] Brightening + CLAHE")
    img_6 = clahe(img_1)
    name_6 = body + ".06.jpg"
    cv2.imwrite(os.path.join(result_path, name_6), img_6)


    #7 C+B write CLAHE + Brightening image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[7/15] CLAHE + Brightening")
    img_7 = brightening(img_3)
    name_7 = body + ".07.jpg"
    cv2.imwrite(os.path.join(result_path, name_7), img_7)


    #8 R+C write Retinex + CLAHE image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[8/15] Retinex + CLAHE")
    img_8 = clahe(img_2)
    name_8 = body + ".08.jpg"
    cv2.imwrite(os.path.join(result_path, name_8), img_8)


    #9 C+R write CLAHE + Retinex image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[9/15] CLAHE + Retinex")
    img_9 = MSRCR(img_3,config['sigma_list'],config['G'],config['b'],config['alpha'],config['beta'],config['low_clip'],config['high_clip'])
    name_9 = body + ".09.jpg"
    cv2.imwrite(os.path.join(result_path, name_9), img_9)


    #10 B+R+C write Brightening + Retinex + CLAHE image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[10/15] Brightening + Retinex + CLAHE")
    img_10 = clahe(img_4)
    name_10 = body + ".10.jpg"
    cv2.imwrite(os.path.join(result_path, name_10), img_10)


    #11 B+C+R write Brightening + CLAHE + Retinex image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[11/15] Brightening + CLAHE + Retinex")
    img_11 = MSRCR(img_6,config['sigma_list'],config['G'],config['b'],config['alpha'],config['beta'],config['low_clip'],config['high_clip'])
    name_11 = body + ".11.jpg"
    cv2.imwrite(os.path.join(result_path, name_11), img_11)


    #12 R+B+C write Retinex + Brightening + CLAHE image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[12/15] Retinex + Brightening + CLAHE")
    img_12 = clahe(img_5)
    name_12 = body + ".12.jpg"
    cv2.imwrite(os.path.join(result_path, name_12), img_12)


    #13 R+C+B write Retinex + CLAHE + Brightening image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[13/15] Retinex + CLAHE + Brightening")
    img_13 = brightening(img_8)
    name_13 = body + ".13.jpg"
    cv2.imwrite(os.path.join(result_path, name_13), img_13)


    #14 C+B+R write CLAHE + Brightening + Retinex image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[14/15] CLAHE + Brightening + Retinex")
    img_14 = MSRCR(img_7,config['sigma_list'],config['G'],config['b'],config['alpha'],config['beta'],config['low_clip'],config['high_clip'])
    name_14 = body + ".14.jpg"
    cv2.imwrite(os.path.join(result_path, name_14), img_14)


    #15 C+R+B write CLAHE + Retinex + Brightening image file into result document
    print("  ", time.strftime("%H:%M:%S", time.localtime()), "[15/15] CLAHE + Retinex + Brightening")
    img_15 = brightening(img_9)
    name_15 = body + ".15.jpg"
    cv2.imwrite(os.path.join(result_path, name_15), img_15)
    

    print("Processing finished: ", img_name)




#img_result_list = os.listdir(result_path)

#for img_name in img_result_list:
#    img = cv2.imread(os.path.join(result_path, img_name))
#    print(time.strftime("%H:%M:%S", time.localtime()), "Processing Image Histogram: ", img_name)
    #img_ih = ih(img)
    
#    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#    img_ih = plt.hist(img.ravel(), 256, [0,256])
    
#    body, ext = os.path.splitext(img_name)
#    name = body + "_IH.png"
#    plt.imsave(os.path.join(result_ih_path, name), img_ih)





'''
if not os.path.exists('result'):
    os.mkdir('result')

image_files = [join('images', f) for f in listdir('images') if isfile(join('images', f))]
for f in image_files:
    print("processing " + f)
    img = cv2.imread(f, cv2.IMREAD_COLOR)
    height = img.shape[0] // 5
    width = img.shape[1] // 5
    dim = (width, height)
    #img = cv2.resize(img, dim)
    # cv2.imshow('img', clahe_img)
    # cv2.waitKey(0)

    brightening_img = brightening(img)
    clahe_img = clahe(brightening_img)

    cv2.imwrite(f.replace('images', 'result'), clahe_img)
'''