import cv2
import numpy as np

MANGO_REGION_LOW_LIMIT = 25
MANGO_REGION_HIGH_LIMIT = 256
MANGO_DISEASED_LOW_LIMIT = 120
MANGO_DISEASED_HIGH_LIMIT = 140
MANGO_MATURITY_LOW_LIMIT = 100
MANGO_MATURITY_HIGH_LIMIT = 125

MANGO_UNKNOWN = -1
MANGO_SMALL = 0
MANGO_MEDIUM = 1
MANGO_BIG = 2
MANGO_VERY_BIG = 3

MANGO_UNKNOWN_Q = -1
MANGO_POOR_Q = 0
MANGO_MEDIUM_Q = 1
MANGO_GOOD_Q = 2
MANGO_EXCELLENT_Q = 3

MINOR_LIMIT_1 = 0.2
MINOR_LIMIT_2 = 0.3
MINOR_LIMIT_3 = 0.4

MAJOR_LIMIT_1 = 0.2
MAJOR_LIMIT_2 = 0.4
MAJOR_LIMIT_3 = 0.6


def classify_minor_axis(value):
    if value > 0 and value <= MINOR_LIMIT_1:
        return MANGO_SMALL
    elif value > MINOR_LIMIT_1 and value <= MINOR_LIMIT_2:
        return MANGO_MEDIUM
    elif value > MINOR_LIMIT_2 and value <= MINOR_LIMIT_3:
        return MANGO_BIG
    elif value > MINOR_LIMIT_3 and value <= 1:
        return MANGO_VERY_BIG
    else:
        return MANGO_UNKNOWN


def classify_major_axis(value):
    if value > 0 and value <= MAJOR_LIMIT_1:
        return MANGO_SMALL
    elif value > MAJOR_LIMIT_1 and value <= MAJOR_LIMIT_2:
        return MANGO_MEDIUM
    elif value > MAJOR_LIMIT_2 and value <= MAJOR_LIMIT_3:
        return MANGO_BIG
    elif value > MAJOR_LIMIT_3 and value <= 1:
        return MANGO_VERY_BIG
    else:
        return MANGO_UNKNOWN


def calc_mango_quality(major, minor):
    class_major = classify_major_axis(major)
    class_minor = classify_minor_axis(minor)
    if class_minor == MANGO_SMALL or class_major == MANGO_SMALL:
        return MANGO_POOR_Q
    elif class_minor == MANGO_MEDIUM or class_major == MANGO_MEDIUM:
        return MANGO_MEDIUM_Q
    elif class_minor == MANGO_BIG or class_major == MANGO_BIG:
        return MANGO_GOOD_Q
    elif class_minor == MANGO_VERY_BIG and class_major == MANGO_VERY_BIG:
        return MANGO_EXCELLENT_Q
    else:
        return MANGO_UNKNOWN_Q


def calc_mango_feats(filename):
    # read image
    img = cv2.imread(filename)

    if img is None:
        raise ValueError('Image {} could not be read'.format(filename))

    # remove noise
    median = cv2.medianBlur(img, 9)

    # binary from saturation channel
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    _, binary = cv2.threshold(
        hsv[:, :, 1],
        MANGO_REGION_LOW_LIMIT,
        MANGO_REGION_HIGH_LIMIT,
        cv2.THRESH_BINARY)

    # find contours to limit mango area
    imgc, contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # find the main contour (this is the one that limits the mango area)
        main_contour = max(contours, key=cv2.contourArea)

        # get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(main_contour)

        # get the ROI of initial image and binary
        roi = img[y:y+h, x:x+w, :]
        roi_binary = binary[y:y+h, x:x+w]

        # ROI in RGB
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

        # convert to CIELab for disease analysis
        lab = cv2.cvtColor(roi, cv2.COLOR_BGR2Lab)

        # total number of pixels of mango
        mango_indices = np.where(roi_binary == 255)
        n_mango_pixels = len(mango_indices[0])

        # pixels of diseased areas
        condition_dis = np.logical_and(
            roi_binary == 255,
            np.logical_and(
                lab[:, :, 2] >= MANGO_DISEASED_LOW_LIMIT,
                lab[:, :, 2] <= MANGO_DISEASED_HIGH_LIMIT))
        diseased_pixels = np.where(condition_dis)
        n_diseased_pixels = len(diseased_pixels[0])

        # pixels of healthy areas
        condition_hea = np.logical_and(
            roi_binary == 255,
            lab[:, :, 2] > MANGO_DISEASED_HIGH_LIMIT)
        healthy_pixels = np.where(condition_hea)
        n_healthy_pixels = len(healthy_pixels[0])

        # Color healthy areas as green and diseased ones as red
        roi_diseased = np.copy(roi_rgb)
        roi_diseased[diseased_pixels[0],
                     diseased_pixels[1], :] = [255, 0, 0]
        roi_diseased[healthy_pixels[0],
                     healthy_pixels[1], :] = [0, 255, 0]

        # pixels of unripe areas
        condition_unripe = np.logical_and(
            roi_binary == 255,
            np.logical_and(
                lab[:, :, 1] >= MANGO_MATURITY_LOW_LIMIT,
                lab[:, :, 1] <= MANGO_MATURITY_HIGH_LIMIT,
            )
        )
        unripe_pixels = np.where(condition_unripe)
        n_unripe_pixels = len(unripe_pixels[0])

        # pixels of ripe areas
        conditioin_ripe = np.logical_and(
            roi_binary == 255,
            lab[:, :, 1] > MANGO_MATURITY_HIGH_LIMIT
        )
        ripe_pixels = np.where(conditioin_ripe)
        n_ripe_pixels = len(ripe_pixels[0])

        # Color ripe areas as yellow and unripe as green
        roi_maturity = np.copy(roi_rgb)
        roi_maturity[unripe_pixels[0],
                     unripe_pixels[1], :] = [0, 255, 0]
        roi_maturity[ripe_pixels[0],
                     ripe_pixels[1], :] = [255, 255, 0]

        # max length of mango
        h, w, d = img.shape
        max_length = max(h, w)

        # normalized major and minor axes
        h, w, d = roi.shape
        major = max(h, w) / max_length
        minor = min(h, w) / max_length

        return(
            round(100 * n_diseased_pixels / n_mango_pixels, 2),
            round(100 * n_healthy_pixels / n_mango_pixels, 2),
            round(100 * n_unripe_pixels / n_mango_pixels, 2),
            round(100 * n_ripe_pixels / n_mango_pixels, 2),
            major,
            minor,
            roi_rgb,
            roi_diseased,
            roi_maturity
        )
    else:
        return(
            -1, -1, -1, -1, -1, -1, None, None, None
        )
