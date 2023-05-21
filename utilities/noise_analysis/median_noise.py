from posixpath import splitext
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from os.path import basename

def median_noise_inconsistencies(image_path, n_size = 3):
    # print("Analyzing...")
    # bar = progressbar.ProgressBar(maxval=20,
    #                               widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    # bar.start()

    img = cv.imread(image_path)
    img_rgb = img[:, :, ::-1]

    flatten = True
    multiplier = 10
    
    # bar.update(5)

    img_filtered = img

    img_filtered = cv.medianBlur(img, n_size)

    noise_map = np.multiply(np.absolute(img - img_filtered), multiplier)
    # bar.update(15)

    if flatten == True:
        #noise_map = np.average(noise_map,axis=-1)
        noise_map = cv.cvtColor(noise_map, cv.COLOR_BGR2GRAY)
    # bar.update(20)
    # bar.finish()
    # print("Done")

    
    plt.subplot(1, 1, 1), plt.imshow(noise_map)
    plt.xticks([]), plt.yticks([])
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.axis('off')

    # Save the result to a file
    output_path = splitext(image_path)[0] + "_Noise_median_output.jpg"
    plt.savefig(output_path)
    return output_path