import logging
import os
from easyocr import easyocr

from utils.utils import  align_text_arabic
from paddleocr import PaddleOCR

os.environ["KMP_DUPLICATE_LIB_OK"] = 'True'


class arabic_ocr:

    def __init__(self):
        self.detector = PaddleOCR(use_angle_cls=True, lang='ar')
        self.ocr = easyocr.Reader(["ar"], detector=False, recognizer=True)

    def get_ocr_results(self, image):
        return self.detector.ocr(image, det=True, rec=True)

    def recognize_text(self, image):
        return self.ocr.recognize(image)

    def get_results(self, image):
        results = self.get_ocr_results(image)
        boxes = [line[0] for line in results[0]]
        texts = [line[1][0] for line in results[0]]
        confidence_score = [line[1][1] for line in results[0]]
        text_score = []
        for box, text, score in zip(boxes, texts, confidence_score):
            x_min, y_min, x_max, y_max = int(box[0][0]), int(box[0][1]), int(box[2][0]), int(box[2][1])
            if isinstance(box, list) and all(isinstance(coord, list) for coord in box):
                cropped_text = image[y_min:y_max, x_min:x_max]
                easyocr_text = self.recognize_text(cropped_text)[0][1][::-1]
                print(easyocr_text)
                text_score.append((easyocr_text, score))
            else:
                raise TypeError("box must be a list of lists with coordinates")
        results = [[box, text_score[idx]] for idx, box in enumerate(boxes)]
        return results

    def ocr_layout(self, image, alignment_tolerance=10):

        font = "arabic.ttf"
        ocr_results = self.get_results(image)
        print(f"results {ocr_results}\n\n")

        if ocr_results is not None:
            boxes = [line[0] for line in ocr_results]
            texts = [line[1][0] for line in ocr_results]
            scores = [line[1][1] for line in ocr_results]

            text = align_text_arabic(ocr_results, alignment_tolerance)

            return None, text

        else:
            return None, ""
