from itertools import compress
from os.path import splitext
import sys
from PIL import Image
import cv2 as cv
import numpy as np
from skimage import color as sci_color



class CloneDetector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None

    def detect_cloning(self):
        image = Image.open(self.image_path)
        image = image.convert('RGB')
        img = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        detector = cv.BRISK_create()
        kpts, desc = detector.detectAndCompute(gray, None)

        matcher = cv.BFMatcher_create(cv.NORM_HAMMING, True)
        matches = matcher.radiusMatch(desc, desc, 20)
        matches = [item for sublist in matches for item in sublist]
        matches = [m for m in matches if m.queryIdx != m.trainIdx]

        clusters = []
        min_dist = 0.15 * np.min(gray.shape) / 2
        kpts_a = np.array([p.pt for p in kpts])
        ds = np.linalg.norm([kpts_a[m.queryIdx] - kpts_a[m.trainIdx] for m in matches], axis=1)
        matches = [m for i, m in enumerate(matches) if ds[i] > min_dist]

        total = len(matches)
        for i in range(total):
            match0 = matches[i]
            d0 = ds[i]
            query0 = match0.queryIdx
            train0 = match0.trainIdx
            group = [match0]

            for j in range(i + 1, total):
                match1 = matches[j]
                query1 = match1.queryIdx
                train1 = match1.trainIdx
                if query1 == train0 and train1 == query0:
                    continue
                d1 = ds[j]
                if np.abs(d0 - d1) > min_dist:
                    continue

                a0 = np.array(kpts[query0].pt)
                b0 = np.array(kpts[train0].pt)
                a1 = np.array(kpts[query1].pt)
                b1 = np.array(kpts[train1].pt)

                aa = np.linalg.norm(a0 - a1)
                bb = np.linalg.norm(b0 - b1)
                ab = np.linalg.norm(a0 - b1)
                ba = np.linalg.norm(b0 - a1)

                if not (0 < aa < min_dist and 0 < bb < min_dist or 0 < ab < min_dist and 0 < ba < min_dist):
                    continue
                for g in group:
                    if g.queryIdx == train1 and g.trainIdx == query1:
                        break
                else:
                    group.append(match1)

            clusters.append(group)

        output = np.copy(image)
        hsv = np.zeros((1, 1, 3))

        for c in clusters:
            for m in c:
                ka = kpts[m.queryIdx]
                pa = tuple(map(int, ka.pt))
                sa = int(np.round(ka.size))
                kb = kpts[m.trainIdx]
                pb = tuple(map(int, kb.pt))
                sb = int(np.round(kb.size))
                angle = np.arctan2(pb[1] - pa[1], pb[0] - pa[0])
                if angle < 0:
                    angle += np.pi
                hsv[0, 0, 0] = angle / np.pi * 180
                hsv[0, 0, 1] = 255
                hsv[0, 0, 2] = m.distance / 20 * 255
                # hsv_color = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
                hsv_color = sci_color.hsv2rgb(hsv / 255.0) * 255
                color = tuple(map(int, hsv_color[0, 0]))
                cv.line(output, pa, pb, color, 2)
                cv.circle(output, pa, sa, color, 2)
                cv.circle(output, pb, sb, color, 2)

        self.image = output
        output_path = splitext(self.image_path)[0] + "_cloning_output.jpg"
        self.image_path = output_path
        cv.imwrite(output_path, self.image)
        return output_path



