from paddleocr import PaddleOCR, draw_ocr
from utils.utils import  align_text
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class OCR:
    def __init__(self, lang="en"):
        self.ocr = PaddleOCR(lang=lang, use_angle_cls=False)
        self.lang = lang

    def __call__(self, image):
        results = self.ocr.ocr(image, det=True, rec=True, cls=True, bin=False)
        return results

    def ocr_layout(self, image, lang, alignment_tolerance):
        if lang == "fr":
            font = "french.ttf"
        elif lang == "en":
            font = "latin.ttf"
        else:
            raise Exception("font not supported for the specified language")
        ocr_results = self.ocr.ocr(image)
        if ocr_results[0] is not None:
            print(ocr_results)
            boxes = [line[0] for line in ocr_results[0]]
            texts = [line[1][0] for line in ocr_results[0]]
            scores = [line[1][1] for line in ocr_results[0]]

            ocr_img = draw_ocr(image, boxes, texts, scores,
                               font_path=os.path.join(main_dir, f"Paddle_fonts/doc/fonts/{font}"))
            # save ocr image

            text = align_text(ocr_results, alignment_tolerance)

            return ocr_img, text

        else:
            return image, ""
