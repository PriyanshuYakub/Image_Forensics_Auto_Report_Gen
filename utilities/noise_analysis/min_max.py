from posixpath import splitext
import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def minmax_dev(patch, mask):
    c = patch[1, 1]
    minimum, maximum, _, _ = cv.minMaxLoc(patch, mask)
    if c < minimum:
        return -1
    if c > maximum:
        return +1
    return 0

def blk_filter(img, radius):
    result = np.zeros_like(img, np.float32)
    rows, cols = result.shape
    block = 2 * radius + 1
    for i in range(radius, rows, block):
        for j in range(radius, cols, block):
            result[i - radius : i + radius + 1, j - radius : j + radius + 1] = np.std(
                img[i - radius : i + radius + 1, j - radius : j + radius + 1]
            )
    return cv.normalize(result, None, 0, 127, cv.NORM_MINMAX, cv.CV_8UC1)

def minmax_noise_analysis(image_path):
    # print(image_path)
    image = cv.imread(image_path)
    if image is None:
        print("Failed to load image.")
        return
    
    channel = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    kernel = 3
    border = kernel // 2
    shape = (channel.shape[0] - kernel + 1, channel.shape[1] - kernel + 1, kernel, kernel)
    strides = 2 * channel.strides
    patches = np.lib.stride_tricks.as_strided(channel, shape=shape, strides=strides)
    patches = patches.reshape((-1, kernel, kernel))
    mask = np.full((kernel, kernel), 255, dtype=np.uint8)
    mask[border, border] = 0
    blocks = [0] * (shape[0] * shape[1])
    
    for i, patch in enumerate(patches):
        blocks[i] = minmax_dev(patch, mask)

    output = np.array(blocks).reshape(shape[:-2])
    output = cv.copyMakeBorder(output, border, border, border, border, cv.BORDER_CONSTANT)
    low = output == -1
    high = output == +1
    
    radius = 3  # Set the desired filter radius
    if radius > 0:
        radius += 3
        low_filtered = blk_filter(low, radius)
        high_filtered = blk_filter(high, radius)
        minmax = np.repeat(low_filtered[:, :, np.newaxis], 3, axis=2)
        minmax += np.repeat(high_filtered[:, :, np.newaxis], 3, axis=2)
        minmax = minmax.astype(np.uint8)
    else:
        minmax = np.zeros_like(image)
        minmax[low] = [0, 0, 255]
        minmax[high] = [255, 255, 255]

    # Show the result
    plt.imshow(cv.cvtColor(minmax, cv.COLOR_BGR2RGB))
    
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.axis('off')

    # Save the result to a file
    output_path = splitext(image_path)[0] + "_Noise_min_max_output.jpg"
    plt.savefig(output_path)
    return output_path