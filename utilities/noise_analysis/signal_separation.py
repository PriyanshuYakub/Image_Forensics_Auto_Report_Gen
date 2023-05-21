from posixpath import splitext
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import xgboost as xgb


def pad_image(image, block):
    rows, cols = image.shape[:2]
    padded_rows = rows + (block - rows % block) % block
    padded_cols = cols + (block - cols % block) % block
    padded_image = np.zeros((padded_rows, padded_cols), dtype=np.uint8)
    padded_image[:rows, :cols] = image
    return padded_image

def ssim(a, b, maximum=255):
    c1 = (0.01 * maximum) ** 2
    c2 = (0.03 * maximum) ** 2
    k = (11, 11)
    s = 1.5
    a2 = a ** 2
    b2 = b ** 2
    ab = a * b
    mu_a = cv.GaussianBlur(a, k, s)
    mu_b = cv.GaussianBlur(b, k, s)
    mu_a2 = mu_a ** 2
    mu_b2 = mu_b ** 2
    mu_ab = mu_a * mu_b
    s_a2 = cv.GaussianBlur(a2, k, s) - mu_a2
    s_b2 = cv.GaussianBlur(b2, k, s) - mu_b2
    s_ab = cv.GaussianBlur(ab, k, s) - mu_ab
    t1 = 2 * mu_ab + c1
    t2 = 2 * s_ab + c2
    t3 = t1 * t2
    t1 = mu_a2 + mu_b2 + c1
    t2 = s_a2 + s_b2 + c2
    t1 *= t2
    s_map = cv.divide(t3, t1)
    return cv.mean(s_map)[0]


def get_metrics(pristine, distorted):
    # Matrix precomputation
    x0 = pristine.astype(np.float64)
    y0 = distorted.astype(np.float64)
    x2 = np.sum(np.square(x0))
    y2 = np.sum(np.square(y0))
    xs = np.sum(x0)
    e = x0 - y0
    maximum = 255
    # Feature vector initialization
    m = np.zeros(8)
    # Mean Square Error (MSE)
    m[0] = np.mean(np.square(e))
    # Peak to Signal Noise Ratio (PSNR)
    m[1] = 20 * np.log10(maximum / np.sqrt(m[0])) if m[0] > 0 else -1
    # Normalized Cross-Correlation (NCC)
    m[2] = np.sum(x0 * y0) / x2 if x2 > 0 else -1
    # Average Difference (AD)
    m[3] = np.mean(e)
    # Structural Content (SC)
    m[4] = x2 / y2 if y2 > 0 else -1
    # Maximum Difference (MD)
    m[5] = np.max(e)
    # Normalized Absolute Error (NAE)
    m[6] = np.sum(np.abs(e)) / xs if xs > 0 else -1
    # Structural Similarity (SSIM)
    m[7] = ssim(x0, y0, maximum)
    return m


def get_features(image, windows, levels):
    metrics = 8
    f = np.zeros(windows * levels * metrics)
    index = 0
    for w in range(windows):
        k = 2 * (w + 1) + 1
        previous = image
        for _ in range(levels):
            filtered = cv.medianBlur(previous, k)
            f[index : index + metrics] = get_metrics(previous, filtered)
            index += metrics
            previous = filtered
    return f


def analyze_signal_noise(image_path):
    image = cv.imread(image_path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    modelfile = "median_b64.json"
    booster = xgb.Booster()
    # try:
    booster.load_model(modelfile)
    # except xgb.core.XGBoostError:
    #     # print(f"Unable to load model ({modelfile})!")
    #     return
    columns = booster.num_features()
    if columns == 8:
        levels = 1
        windows = 1
    elif columns == 24:
        levels = 3
        windows = 1
    elif columns == 96:
        levels = 3
        windows = 4
    elif columns == 128:
        levels = 4
        windows = 4
    else:
        print("Unknown model format!")
        return

    block = 16
    padded = pad_image(gray, block)
    rows, cols = padded.shape
    prob = np.zeros(((rows // block) + 1, (cols // block) + 1))
    var = np.zeros_like(prob)
    for i in range(0, rows, block):
        for j in range(0, cols, block):
            roi = padded[i : i + block, j : j + block]
            x = xgb.DMatrix(np.reshape(get_features(roi, levels, windows), (1, columns)))
            y = booster.predict(x)[0]
            ib = i // block
            jb = j // block
            var[ib, jb] = np.var(roi)
            prob[ib, jb] = y

    mask = var < 5  # Example threshold value
    prob = cv.medianBlur(prob.astype(np.float32), 3)
    output = np.repeat(prob[:, :, np.newaxis], 3, axis=2)
    output[mask] = 0
    output = cv.convertScaleAbs(output, None, 255)
    output = cv.resize(output, None, None, block, block, cv.INTER_LINEAR)
    plt.imshow(cv.cvtColor(output, cv.COLOR_BGR2RGB))
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    

    # Save the result to a file
    output_path = splitext(image_path)[0] + "_Noise_signal_separation_output.jpg"
    plt.savefig(output_path)
    


# Usage example:
# image_path = "path_to_your_image.jpg"
# image = cv.imread(image_path)
# output_image = analyze_signal_noise(image)
# cv.imshow("Output", output_image)
# cv.waitKey(0)
# cv.destroyAllWindows()
