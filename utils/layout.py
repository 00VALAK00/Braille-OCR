import os.path
import cv2
from utils.ar_ocr import arabic_ocr
from paddleocr import PPStructure, draw_structure_result, sorted_layout_boxes
from utils.utils import read_img, pad, segment, save_image
from utils.ocr import OCR
import pybrl as brl
import logging
import csv

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')
logger = logging.getLogger("table_detection")

main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def load_model():
    logger.info(f"main {main_dir}")
    logger.info("Started loading model")
    model = PPStructure(show_log=True,
                        lang="en",
                        layout=True,
                        ocr=False,
                        det=False,
                        rec=False,
                        recovery=False,
                        table=False,
                        binarize=False
                        )
    logger.info(f"Layout model has been successfully loaded")
    return model


class Layout_analyzer:
    def __init__(self, lang="en"):
        self.model = load_model()
        self.save_folder = os.path.join(main_dir, "outputs")
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        if lang == "en":
            self.font_dir = os.path.join(main_dir, r"Paddle_fonts/doc/fonts/latin.ttf")
        elif lang == "ar":
            self.font_dir = os.path.join(main_dir, r"Paddle_fonts/doc/fonts/persian.ttf")
        else:
            self.font_dir = os.path.join(main_dir, r"Paddle_fonts/doc/fonts/french.ttf")
        logger.info(f"Language option set to {lang} ")
        self.ocr = OCR(lang=lang) if lang in ["fr", "en"] else arabic_ocr()

    def perform_ocr(self, img_path, segment_img=False, analyze=False, translate=True):
        img_base_name = os.path.basename(img_path).split('.')[0]
        dir_path = os.path.join(self.save_folder, f"{img_base_name}")

        img = read_img(img_path)
        img = segment(img) if segment_img else img

        if analyze:
            logger.info("Analyse parameter has been set to True. Performing layout analysis coupled with ocr")
            h, w = img.shape[0], img.shape[1]
            results = self.model(img)
            results = pad(results, padding=0)
            results = sorted_layout_boxes(results, w)
            im_show = self.draw_structure_results(img, results)
            self.save_structure_results(img_path, im_show)
            for i, layout in enumerate(results):

                bbox = layout["bbox"]
                layout_type = layout["type"]
                x_min, y_min, x_max, y_max = bbox[0], bbox[1], bbox[2], bbox[3]
                layout_img = img[y_min:y_max, x_min:x_max]
                if isinstance(self.ocr, OCR):
                    if layout_type in ["figure", "table"]:
                        ocr_img, text = self.ocr.ocr_layout(layout_img, self.ocr.lang, alignment_tolerance=10)
                    else:
                        ocr_img, text = self.ocr.ocr_layout(layout_img, self.ocr.lang, alignment_tolerance=10)


                else:
                    if layout_type in ["figure", "table"]:
                        ocr_img, text = self.ocr.ocr_layout(layout_img, alignment_tolerance=20)
                    else:
                        ocr_img, text = self.ocr.ocr_layout(layout_img, alignment_tolerance=30)

                with open(os.path.join(dir_path, "ocr.txt"), newline='', mode="a", encoding="utf_8") as f:
                    writer = csv.writer(f)
                    for line in text:
                        if isinstance(self.ocr, arabic_ocr):
                            line = line[::-1]
                            writer.writerow([line])
                        else:
                            writer.writerow([line])
                if translate:
                    with open(os.path.join(dir_path, "braille_translation_grid2.txt"), newline='', mode="a",
                              encoding="utf_8") as f:
                        writer = csv.writer(f)
                        for line in text:
                            if not isinstance(self.ocr, arabic_ocr):
                                # cannot translate arabic with current package (pybrl)
                                braille_grid_rep = brl.translate(line)
                                unicode_rep = brl.toUnicodeSymbols(braille_grid_rep, flatten=True)
                                writer.writerow([unicode_rep])



        else:
            # if we need not perform layout detection
            logger.info("Analyse parameter has been set to False. Limiting only to text detection and recognition")
            ocr_img, text = self.ocr.ocr_layout(img, self.ocr.lang, alignment_tolerance=10) if isinstance(self.ocr,
                                                                                                          OCR) else self.ocr.ocr_layout(
                img, alignment_tolerance=10)
            os.makedirs(dir_path, exist_ok=True)
            if ocr_img is not None:
                save_image(ocr_img, os.path.join(dir_path, f"OCR_{img_base_name}.jpg"), )

            with open(os.path.join(dir_path, "ocr.txt"), newline='', mode="w", encoding="utf_8") as f:
                writer = csv.writer(f)
                for line in text:
                    if isinstance(self.ocr, arabic_ocr):
                        line = line[::-1]
                        writer.writerow([line])
                    else:
                        writer.writerow([line])

            if translate:
                with open(os.path.join(dir_path, "braille_translation_grid2.txt"), newline='', mode="a",
                          encoding="utf_8") as f:
                    writer = csv.writer(f)
                    for line in text:
                        if not isinstance(self.ocr, arabic_ocr):
                            braille_grid_rep = brl.translate(line)
                            unicode_rep = brl.toUnicodeSymbols(braille_grid_rep, flatten=True)
                            writer.writerow([unicode_rep])

    def draw_structure_results(self, image, results):
        im_show = draw_structure_result(image, results, font_path=self.font_dir)
        return im_show

    def save_structure_results(self, img_path: str, image):
        save_folder = os.path.join(self.save_folder, os.path.basename(img_path).split(".")[0])
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        cv2.imwrite(os.path.join(save_folder, os.path.basename(img_path).split(".")[0] + ".jpg"), image)
