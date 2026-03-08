import time
import pytesseract
from PIL import ImageGrab
import pyautogui
import pygetwindow as gw
import pyperclip
import json


# ==============================
# 1 Tesseract路径
# ==============================

pytesseract.pytesseract.tesseract_cmd = r"C:\MSWBID\python\projects\tesseract-ocr\tesseract.exe"
filepath=r"C:\MSWBID\python\projects\wxbot\history.json" #对话历史

# ==============================
# 2 获取微信窗口
# ==============================
def get_4mouse_position():
    time.sleep(3)
    positions=[]
    for i in range(4):
        time.sleep(2)
        positions.append(pyautogui.position())
        print(positions[i],"record")
    print(positions)

def get_wechat_window():

    windows = gw.getWindowsWithTitle("微信")

    if not windows:
        print("未找到微信窗口")
        return None

    return windows[0]


# ==============================
# 3 计算聊天区域
# ==============================

def get_chat_region():

    win = get_wechat_window()

    if win is None:
        return None

    left = win.left
    top = win.top
    width = win.width
    height = win.height

    """
    微信窗口结构：

    左侧：聊天列表
    右侧：聊天内容
    底部：输入框

    我们只截取
    右侧聊天区域的底部
    """

    chat_left = left + int(width * 0.3)
    chat_right = left + width

    chat_top = top + int(height * 0.55)
    chat_bottom = top + int(height)

    return (chat_left, chat_top, chat_right, chat_bottom)


# ==============================
# 4 获取最后消息坐标
# ==============================

def get_last_message_pos():

    win = get_wechat_window()

    left = win.left
    top = win.top
    width = win.width
    height = win.height

    x = left + int(width * 0.75)
    y = top + int(height * 0.75)

    return (x, y)


# ==============================
# 5 截图
# ==============================

def capture_region():

    region = get_chat_region()

    if region is None:
        return None

    img = ImageGrab.grab(bbox=region)

    return img


# ==============================
# 6 OCR识别
# ==============================

def ocr_image(img):

    text = pytesseract.image_to_string(
        img,
        lang="chi_sim"
    )
    print(text)
    return text.strip()


# ==============================
# 7 复制消息
# ==============================

def copy_message():

    # x, y = get_last_message_pos()
    time.sleep(1)
    pyautogui.moveTo(1812,782, duration=0.1)

    pyautogui.rightClick()

    time.sleep(1)
    pyautogui.moveRel(10,-40)
    pyautogui.leftClick()
    time.sleep(1)
    pyautogui.moveTo(1325, 786, duration=0.1)
    pyautogui.rightClick()
    time.sleep(1)
    pyautogui.moveRel(10, -40)
    pyautogui.leftClick()
    time.sleep(1)
    # pyautogui.keyDown("esc")
    return pyperclip.paste()


# ==============================
# 8 主循环
# ==============================

def listen_loop(history_len):

    last_text = ""

    print("开始监听微信消息...")

    while True:
        msg_history = read_file(filepath)

        img = capture_region()

        if img is None:
            time.sleep(1)
            continue

        text = ocr_image(img)

        if text and text != last_text:

            print("检测到消息变化")

            msg = copy_message()

            print("新消息:", msg)
            try:
                if msg!=msg_history[-1]:
                    msg_history.append(msg)
            except:
                msg_history=[]
                msg_history.append(msg)
            last_text = text
            print("当前消息历史",msg_history)
            write_file(filepath,rearrange_file(msg_history,history_len))
        time.sleep(0.5)


def write_file(file_path,messages):
    # 保存到文件
    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False)


def read_file(file_path):
    # 读取回列表
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_messages = json.load(f)

    return loaded_messages

def rearrange_file(msg,depth):
    while True:
        if len(msg)>depth:
            msg.pop(0)
        else:
            break
    return msg
# ==============================
# 9 程序入口
# ==============================
if __name__ == "__main__":
    listen_loop(3)