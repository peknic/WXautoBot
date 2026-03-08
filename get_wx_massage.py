import time
from PIL import ImageGrab
import pyautogui
import pygetwindow as gw
import pyperclip
import json
from paddleocr import PaddleOCR
import cv2
import numpy as np
import pygetwindow as gw
#初始化paddleocr
ocr = PaddleOCR(
    lang="ch",       # 中文
    use_angle_cls=True,
    show_log=False
)
filepath=r"C:\MSWBID\python\projects\wxbot\history.json" #对话历史
#创捷对话历史文件
with open(filepath, "w+", encoding="utf-8") as f:
    json.dump([{"role":"user","content":"init"}], f, ensure_ascii=False)
def focus_window():
    win = gw.getWindowsWithTitle('微信')[0]
    if win:
        win.activate()
# 获取所有窗口对象
def get_all_windows_title():#获取所有窗口的标题
    all_windows = gw.getAllWindows()

    print(f"当前共检测到 {len(all_windows)} 个窗口：\n")

    # for win in all_windows:
    #     # 过滤掉标题为空的窗口（很多后台系统小组件标题为空）
    #     if win.title:
    #         print(f"- 标题: {win.title}")
    #         # 如果你想看更多信息，可以取消下面这行的注释
    #         print(f"  位置: ({win.left}, {win.top}), 尺寸: {win.width}x{win.height}")
    return all_windows
def find_windows(windows,target_window):#看看设定的目标窗口是否在已打开的窗口里面，返回T/F
    match=0
    for win in windows:
        # 过滤掉标题为空的窗口（很多后台系统小组件标题为空）
        if win.title:
            if target_window in win.title:
                match+=1
    if match!=0:
        return True
    else:
        return False
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

    chat_top = top + int(height * 0.6)
    chat_bottom = top + int(height*0.8)

    return (chat_left, chat_top, chat_right, chat_bottom)
def check_chat_region():#通过鼠标移动来查看聊天框位置
    time.sleep(2)
    pyautogui.moveTo(get_chat_region()[0], get_chat_region()[1], duration=1)
    time.sleep(1)
    pyautogui.moveTo(get_chat_region()[0], get_chat_region()[3], duration=1)
    time.sleep(1)
    pyautogui.moveTo(get_chat_region()[2], get_chat_region()[1], duration=1)
    time.sleep(1)
    pyautogui.moveTo(get_chat_region()[2], get_chat_region()[3], duration=1)
    time.sleep(1)
# ==============================
# 4 获取最后消息坐标
# ==============================
# def get_last_message_pos():
#
#     win = get_wechat_window()
#
#     left = win.left
#     top = win.top
#     width = win.width
#     height = win.height
#
#     x = left + int(width * 0.75)
#     y = top + int(height * 0.75)
#
#     return (x, y)
# ==============================
# 5 截图
# ==============================
def capture_region():

    region = get_chat_region()

    if region is None:
        return None

    img = ImageGrab.grab(bbox=region)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # img.show()
    return img
# ==============================
# 6 OCR识别
# ==============================
def ocr_image(img):
    """
    使用PaddleOCR识别图片并返回字符串

    参数
    -------
    img : numpy.ndarray
        OpenCV格式图片

    返回
    -------
    str
        识别到的文字
    """

    result = ocr.ocr(img)

    if result[0] is None:
        return ""

    texts = []

    for line in result[0]:

        text = line[1][0]  # 识别到的文字
        texts.append(text)
    # print("\n".join(texts))
    return "\n".join(texts)
# ==============================
# 7 复制消息
# ==============================
def copy_message():

    # x, y = get_last_message_pos()
    time.sleep(1)
    pyautogui.moveTo(1812,782, duration=0.1)

    pyautogui.rightClick()

    time.sleep(0.2)
    pyautogui.moveRel(10,-40)
    pyautogui.leftClick()
    time.sleep(0.2)
    pyautogui.moveTo(1325, 786, duration=0.1)
    pyautogui.rightClick()
    time.sleep(0.2)
    pyautogui.moveRel(10, -40)
    pyautogui.leftClick()
    time.sleep(1)
    if find_windows(get_all_windows_title(),"图片"):
        pyautogui.keyDown("esc")
    return pyperclip.paste()
# ==============================
# 8 主循环
# ==============================
def listen_loop(history_len):

    last_text = ""

    print("开始监听微信消息...")
    focus_window()
    while True:
        msg_history = read_file(filepath)

        img = capture_region()

        if img is None:
            time.sleep(1)
            continue

        text = ocr_image(img)

        if text and text != last_text:

            print("检测到消息变化")

            msg = {"role":"user","content":copy_message()}

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
    listen_loop(10)
    # print(ocr_image(r"C:\Users\qingu\OneDrive\Pictures\Screenshots\231.png"))
    # check_chat_region()