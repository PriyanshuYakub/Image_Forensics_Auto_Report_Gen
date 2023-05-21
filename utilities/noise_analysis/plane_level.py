from posixpath import splitext
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def norm_mat(img, to_bgr=False):
    mat = np.amax(img)
    return (img / mat * 255).astype(np.uint8) if to_bgr else img / mat

class PlanesAnalysis:
    def __init__(self, image_path):
        self.image_path = image_path

    def preprocess(self):
        img = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
        self.planes = [np.bitwise_and(np.full_like(img, 2 ** b), img) for b in range(8)]

    def process(self):
        self.preprocess()
        for plane_index, plane in enumerate(self.planes):
            plane = cv.medianBlur(plane, 3)
            plt.subplot(2, 4, plane_index + 1)
            plt.imshow(plane, cmap='gray')
            plt.title(f'Bit Plane {plane_index}')
            plt.xticks([])
            plt.yticks([])
            
        plt.tight_layout()
        # plt.show()
        
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        output_path = splitext(self.image_path)[0] + "_Noise_bit_plane_output.jpg"
    
        plt.savefig(output_path)
        return output_path

# if __name__ == "__main__":
#     image_path = "path_to_your_image.jpg"  # Replace with the path to your image
#     noise_analysis = PlanseAnalysis(image_path)
#     noise_analysis.preprocess()
#     noise_analysis.process()
