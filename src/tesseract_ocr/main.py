import argparse
import os

import cv2
import imutils
import numpy as np
import pytesseract
from imutils.perspective import four_point_transform
from .utils import process_receipt_image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--image", type=str, required=True, help="path to input image"
    )
    args = parser.parse_args()

    # check if image with given path exists
    if not os.path.exists(args.image):
        raise Exception("The given image does not exist.")

    # load the image
    img_orig = cv2.imread(args.image)

    receipt = process_receipt_image(img_orig)

    # apply OCR to the receipt image by assuming column data, ensuring
    # the text is *concatenated across the row* (additionally, for your
    # own images you may need to apply additional processing to cleanup
    # the image, including resizing, thresholding, etc.)
    options = "--psm 6"
    text = pytesseract.image_to_string(
        cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB), config=options
    )
    # show the raw output of the OCR process
    print("[INFO] raw output:")
    print("==================")
    print(text)
    print("\n")


if __name__ == "__main__":
    main()
