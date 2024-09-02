import os.path
from utils.layout import Layout_analyzer
import argparse


def main():
    """
    performs both layout detection & OCR on a given image or directory

    :return:
    creates a directory containing the  csv file
    """

    parser = argparse.ArgumentParser("Perform OCR on a directory")
    parser.add_argument("-d", "--directory", required=True, help="Directory containing images")
    parser.add_argument("-s", "--segment", default=False, help="Segment the image before OCR")
    parser.add_argument("-l", "--language", default="en", help="OCR language", choices=["en", "fr", "ar"])
    parser.add_argument("--analyse", default=True, help="Perform layout detection and OCR on images")
    args = parser.parse_args()

    la = Layout_analyzer(lang=args.language)

    for image_base_name in os.listdir(args.directory):
        image_path = os.path.join(args.directory, image_base_name)
        la.perform_ocr(image_path, False, analyze=False,translate=True)





if __name__ == "__main__":
    main()
