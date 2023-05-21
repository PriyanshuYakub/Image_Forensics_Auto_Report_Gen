from posixpath import splitext
import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

from os.path import basename

def ela(image_path, quality = 90, block_size = 8):
    # print("Analyzing...")
    
    
    img = cv.imread(image_path)
    img_rgb = img[:, :, ::-1]

    # Get the name of the image
    base = basename(image_path)
    file_name = os.path.splitext(base)[0]
    save_file_name = splitext(image_path)[0]+file_name+"_temp.jpg"

   
    multiplier = 15
    flatten = True

    # Resaved the image with the new quality
    encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
    cv.imwrite(save_file_name, img, encode_param)
    # bar.update(10)

    # Load resaved image
    img_low = cv.imread(save_file_name)
    img_low = img_low[:, :, ::-1]

    ela_map = np.zeros((img_rgb.shape[0], img_rgb.shape[1], 3))

    ela_map = np.absolute(1.0*img_rgb - 1.0*img_low)*multiplier

    # bar.update(15)
    if flatten == True:
        ela_map = np.average(ela_map, axis=-1)
    # bar.update(20)
    # bar.finish()
    # print("Done")
    plt.imshow(ela_map), 
    plt.xticks([]), plt.yticks([])
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    output_path = splitext(image_path)[0] + "_ELA_output.jpg"
    
    plt.savefig(output_path)


    os.remove(save_file_name)
    return output_path