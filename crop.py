import cv2
import numpy as np
#from os import listdir
#from os.path import isfile, join
from math import sqrt
import os
import sys
import time
import csv
from matplotlib import pyplot as plt


import json



def crop(img, x, y, height, width):
    img_crop = img[y:y+height, x:x+width]
    return img_crop

def first2(s):
    return s[:2]

def getchar(string, n):
    return str(string)[n - 1]

def noise(img, pts):
    #https://stackoverflow.com/questions/48301186/cropping-concave-polygon-from-image-using-opencv-python/48301735
    pts = np.array(pts)

    ## (1) Crop the bounding rect
    rect = cv2.boundingRect(pts)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()

    ## (2) make mask
    pts = pts - pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    ## (3) do bit-op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    return dst

def mask(img, pts):
    #https://stackoverflow.com/questions/48301186/cropping-concave-polygon-from-image-using-opencv-python/48301735
    pts = np.array(pts)

    ## (1) Crop the bounding rect
    rect = cv2.boundingRect(pts)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()

    ## (2) make mask
    pts = pts - pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    ## (3) do bit-op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    return mask

def show(first, second, third, first_label, second_label, third_label):
    plt.subplot(131),plt.imshow(first,cmap = 'gray')
    plt.title(first_label), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(second,cmap = 'gray')
    plt.title(second_label), plt.xticks([]), plt.yticks([])
    plt.subplot(133),plt.imshow(third,cmap = 'gray')
    plt.title(third_label), plt.xticks([]), plt.yticks([])

    plt.show()

#data_path = "data"
result_path = "Image/result_process"
#result_ih_path = "result_ih"
#result_sobel_path = "result_sobel"
#result_sobel_ih_path = "result_sobel_ih"
result_canny = "Image/result_canny"
result_crop = "Image/result_crop"
result_noise = "Image/result_noise"
result_mask = "Image/mask"
result_dir = "Result"

img_result_list = os.listdir(result_path)
img_result_crop = os.listdir(result_crop)
img_result_canny = os.listdir(result_canny)
img_result_noise = os.listdir(result_noise)
img_mask = os.listdir(result_mask)
result_dir = os.listdir(result_dir)



with open('config.json', 'r') as f:
    config = json.load(f)

#Crop the starfishes from images
for img_name in img_result_list:
    img = cv2.imread(os.path.join(result_path, img_name))

    img_number = first2(img_name)
    print(time.strftime("%H:%M:%S", time.localtime()), "Crop image:", img_name)
    #print("Crop image:", img_name)

    crop_number = len(config[img_number])
    print("Number of crop:", crop_number)

    for i in range(crop_number):
        result = crop(img, config[img_number][str(i)]['x'], config[img_number][str(i)]['y'], config[img_number][str(i)]['height'], config[img_number][str(i)]['width'])
        
        body, ext = os.path.splitext(img_name)
        name = body + "_crop_" + str(i) + ".jpg"

        cv2.imwrite(os.path.join(result_crop, name), result)
        print("Image:", name, "save.")

#Canny Edge detection and Noise Reduced process
for img_name in img_result_crop:
    img = cv2.imread(os.path.join(result_crop, img_name))

    #https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    #Get best value for threshold in Canny
    sigma=0.33
    v = np.median(img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    #Canny Edge detection process
    edges = cv2.Canny(img, lower, upper)

    #get the crop position of image
    img_number = first2(img_name)
    crop_position = getchar(img_name, 12)

    #Reduce the noises outside and inside the starfishes
    pts = config[img_number][str(crop_position)]['mask']
    pts = eval('[' + pts + ']')
    dst = noise(edges, pts)
    mask_img = mask(edges, pts)

    #Display all three images (Original, Canny Edge detection and Noise Reduced) in console
    show(img, edges, dst, 'Original Image', 'Edge Image', 'Noise Reduced Image')
    print(time.strftime("%H:%M:%S", time.localtime()), "Image:", img_name)


    body, ext = os.path.splitext(img_name)

    #Save Canny Edge detection image in result_canny document
    name_canny = body + "_canny.jpg"
    cv2.imwrite(os.path.join(result_canny, name_canny), edges)

    #Save Noise Reduced image in result_noise document
    name_noise = body + "_noise_reduce.jpg"
    cv2.imwrite(os.path.join(result_noise, name_noise), dst)

    #Save Mask Reduced image in result_noise document
    name_mask = body + "_mask.jpg"
    cv2.imwrite(os.path.join(result_mask, name_mask), mask_img)



#Create CSV file for pixel calculation
file_name = "Result/" + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + ".csv"
open(file_name, "x")

#Pixel calculation and result writing
for img_name in img_result_noise:
    img = cv2.imread(os.path.join(result_noise, img_name))

    #Pixel calculation
    n_white_pix = np.sum(img == 255)
    n_black_pix = np.sum(img == 0)
    
    #Result writing
    write_line = img_name + "  " + str(n_white_pix) + "  " + str(n_black_pix)

    text_file = open(file_name, "a")
    n = text_file.write(write_line+ '\n')
    text_file.close()

 
print(time.strftime("%H:%M:%S", time.localtime()), "Pixel calculation result storaged in", file_name)