import pyautogui
import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import ImageGrab



def find_text_on_screen(bbox_crop_region,target_text):
    # 初始化OCR
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)  # 支持中英文
    # 1 截图
    screenshot = ImageGrab.grab(bbox=bbox_crop_region)

    # 转成opencv格式
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 2 OCR识别
    result = ocr.ocr(img)

    # 3 遍历识别结果
    for line in result:
        for word in line:
            box = word[0]  # 文字框四个点
            text = word[1][0]  # 识别的文字
            score = word[1][1]  # 置信度

            # 4 判断目标文字
            if target_text in text:
                # 计算中心坐标
                x = int((box[0][0] + box[2][0]) / 2)
                y = int((box[0][1] + box[2][1]) / 2)

                return {
                    "text": text,
                    "confidence": score,
                    "center": (x, y),
                    "box": box
                }

    return None

if __name__ =="__main__":
    # 示例
    res = find_text_on_screen((0,0,1920,1080),"main")

    print(res)
    if res:
        x, y = res["center"]
        pyautogui.moveTo(x, y,duration=1)