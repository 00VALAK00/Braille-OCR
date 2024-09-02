import cv2
import numpy as np
from pathlib import Path

precedent_path = Path("..")
paddle_path = precedent_path / "Paddle_fonts"


def read_img(img_path):
    return cv2.imread(img_path, cv2.IMREAD_COLOR)


def display_image(image_path):
    cv2.imshow("image", image_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def segment(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # perform thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    display_image(binary)
    enhanced = enhance_words(binary)
    colored = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
    inversed = cv2.bitwise_not(colored)
    display_image(inversed)
    return inversed


def enhance_words(image: np.ndarray):
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(2, 2))
    closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=1)
    dilated = cv2.dilate(closed, kernel)
    return dilated


def pad(results, padding: int):
    for layout in results:
        bbox = layout["bbox"]
        x_min, y_min, x_max, y_max = int(bbox[0]) - padding, int(bbox[1]) - padding, int(bbox[2]) + padding, int(
            bbox[3]) + padding
        layout["bbox"] = [x_min, y_min, x_max, y_max]
    return results


def save_image(img, save_path):
    return cv2.imwrite(save_path, img)


def align_text(results, tolerance):
    boxes = [line[0] for line in results[0]]
    texts = [line[1][0] for line in results[0]]
    confidence_scores = [line[1][1] for line in results[0]]
    text_lines = []
    current_line = ''
    last_y_min = None
    last_y_max = None

    for text, (x1, x2, x3, x4) in zip(texts, boxes):

        y_min = x1[1]
        y_max = x4[1]

        if last_y_min is None:
            current_line = text
        else:
            if abs(y_min - last_y_min) < tolerance and abs(y_max - last_y_max) < tolerance:
                # on same line
                current_line += " " + text
            else:
                # not on the same line
                text_lines.append(current_line)
                current_line = text
        last_y_min = y_min
        last_y_max = y_max

    # append last text
    if current_line:
        text_lines.append(current_line)

    return text_lines


def align_text_arabic(results, tolerance):
    boxes = [line[0] for line in results]
    texts = [line[1][0] for line in results]
    confidence_scores = [line[1][1] for line in results]
    text_lines = []
    current_line = ''
    last_y_min = None
    last_y_max = None

    for text, (x1, x2, x3, x4) in zip(texts, boxes):

        y_min = x1[1]
        y_max = x4[1]

        if last_y_min is None:
            current_line = text
        else:
            if abs(y_min - last_y_min) < tolerance and abs(y_max - last_y_max) < tolerance:
                # on same line
                current_line += " " + text
            else:
                # not on the same line
                text_lines.append(current_line)
                current_line = text
        last_y_min = y_min
        last_y_max = y_max

    # append last text
    if current_line:
        text_lines.append(current_line)

    return text_lines



