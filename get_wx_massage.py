from pywinauto import Application,Desktop

def get_all_windows_name():
    windows = Desktop(backend="uia").windows()
    for w in windows:
        try:
            print("标题:", w.window_text(), "| 类名:", w.class_name())
        except:
            pass

get_all_windows_name()
app_path=r"C:\MSWBID\wechat\新建文件夹\Weixin\Weixin.exe"
app=Application(backend="uia")
app.start(app_path)
app.connect(path=app_path)
win=app.window(title_re="微信")
win.print_control_identifiers()

