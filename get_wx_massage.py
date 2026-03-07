# from pywinauto import Application,Desktop
# from pywinauto.controls.uia_controls import ButtonWrapper
# import time
# import json
#
# def get_all_windows_name():
#     windows = Desktop(backend="uia").windows()
#     for w in windows:
#         try:
#             print("标题:", w.window_text(), "| 类名:", w.class_name())
#         except:
#             pass
#
# get_all_windows_name()
# app_path=r"C:\MSWBID\wechat\wechat\Weixin\Weixin.exe"
# app=Application(backend="uia")
# app.connect(title_re="微信")
# win=app.window(title_re="微信")
# win.print_control_identifiers(depth=10)
# # enter_button:ButtonWrapper=win.child_window(title="进入微信",control_type="Button").wrapper_object()
# # enter_button.click_input()
#
# # chat_list=win.child_window(control_type="List")
# # messages = []
# #
# # last_msg = ""
# #
# # while True:
# #
# #     items = chat_list.descendants(control_type="ListItem")
# #
# #     if items:
# #         last_item = items[-1]
# #
# #         texts = last_item.descendants(control_type="Text")
# #
# #         if len(texts) >= 2:
# #
# #             sender = texts[0].window_text()
# #             content = texts[1].window_text()
# #
# #             msg = sender + ":" + content
# #
# #             if msg != last_msg:
# #
# #                 data = {
# #                     "sender": sender,
# #                     "content": content,
# #                     "time": time.time()
# #                 }
# #
# #                 messages.append(data)
# #
# #                 with open("chat.json","w",encoding="utf8") as f:
# #                     json.dump(messages,f,ensure_ascii=False,indent=2)
# #
# #                 print(sender,":",content)
# #
# #                 last_msg = msg
# #
# #     time.sleep(1)
from pywechat import check_new_message
msg=check_new_message()
print(msg)