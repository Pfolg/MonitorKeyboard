# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME main
AUTHOR Pfolg
TIME 2025/2/17 10:49
"""
import os.path
from datetime import datetime
import time
import tkinter as tk
import pystray
from PIL import Image
import threading
from pynput import keyboard
import json


class MonitorKeyboard:
    def __init__(
            self,name,picture,description,text_bg="#870eb3",
            text_fg="#ffffff",bg="#000000",fg="#ffffff",font=("ariblk.ttf bold", 24),
            sleepTime=.05
    ):
        self.sleepTime=sleepTime
        self.text_bg=text_bg
        self.text_fg=text_fg
        self.bg = bg
        self.fg= fg
        self.font=font
        self.name=name
        self.picture=picture
        # 设定窗口
        self.root=tk.Tk()
        self.set_root()
        self.labelList = [self.label1, self.label2, self.label3]
        # 数据管理
        self.data=[] # [[key,time],[],[]...]
        # 设定托盘菜单
        self.menu=[
            pystray.MenuItem(text='About', action=lambda :os.system("start {}".format(url))),  # 托盘图标控制退出
            pystray.MenuItem(text="Edit in json",action=lambda :os.startfile(config_file)),
            pystray.MenuItem(text='Quit', action=self.quit),# 托盘图标控制退出
        ]
        self.image = Image.open(self.picture)
        self.icon=pystray.Icon(self.name, self.image, description, self.menu)
        # 监视所有键盘按钮->数据
        # 键盘监听
        self.keyboardlistener = keyboard.Listener(
                on_press=self.on_key_press,)
                # on_release=self.on_key_release)

        # 监视所有鼠标按钮->数据
        # 鼠标监听
        # self.mouseListener= mouse.Listener(on_click=self.on_mouse_click)


        # 启动线程

        threading.Thread(target=self.icon.run,daemon=True).start()
        threading.Thread(target=self.manage_data,daemon=True).start()
        self.keyboardlistener.start()
        self.root.mainloop()

    # 定义退出的函数
    def quit(self):
        self.keyboardlistener.stop()
        # self.mouseListener.stop()
        self.root.destroy()
        self.icon.stop()

    def new_closing_window(self):
        pass

    # 设置窗口特性
    def set_root(self):
        # 去除标题栏
        self.root.overrideredirect(True)
        self.root.resizable(False, False)
        # 设置窗口为顶置
        self.root.attributes('-topmost', True)
        # self.root.title(self.name)
        # self.root.iconbitmap(self.picture)
        self.root.configure(background=self.bg)
        self.root.attributes('-transparentcolor', self.bg)
        sw,sh=self.root.winfo_screenwidth(),self.root.winfo_screenheight()
        self.root.geometry("{}x{}+{}+{}".format(int(sw/6),int(sh/5),int(sw/1.3),int(sh/1.5)))
        self.label1=tk.Label(self.root,text="",font=self.font,foreground=self.text_fg,background=self.text_bg)
        self.label2 = tk.Label(self.root,text="", font=self.font,foreground=self.text_fg,background=self.text_bg)
        self.label3 = tk.Label(self.root,text="", font=self.font,foreground=self.text_fg,background=self.text_bg)
        self.label1.pack()
        self.label2.pack()
        self.label3.pack()



        # 绑定窗口的关闭事件->不关闭
        self.root.protocol("WM_DELETE_WINDOW", self.new_closing_window)

    # 按钮按下
    def on_key_press(self, key):
        """处理键盘按下事件"""
        try:
            # 处理普通按键
            key_name = key.char
        except AttributeError:
            # 处理特殊按键
            key_name = key.name.replace('_', ' ').title()
        except NotImplementedError:
            print("Have an error but ignored")
            key_name=None
        self.data.append([key_name,time.localtime()])
        print(self.data[-1])

    # 按钮释放
    def on_key_release(self, key):
        """处理键盘释放事件"""
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name.replace('_', ' ').title()
        except NotImplementedError:
            print("Have an error but ignored")
            key_name=None

        print(key_name)
    # 鼠标按钮
    def on_mouse_click(self, x, y, button, pressed):
        """处理鼠标点击事件"""
        button_name = button.name.title()  # 转换为首字母大写

        # if pressed:
        print(button_name)
    # 主窗口显示




    # 数据管理
    def manage_data(self):
        def struct_time_to_datetime(st):
            """
            将 struct_time 转换为 datetime 对象。
            """
            return datetime.fromtimestamp(time.mktime(st))

        # 计时器，获取输入时刷新，没有输入等待一定时间后清除相应数据->记录日志
        while True:
            x = 0
            try:
                mid_t=str(struct_time_to_datetime(time.localtime())-struct_time_to_datetime(self.data[-1][1])).split(":")
                for i in mid_t:
                    x+=int(i)
            except IndexError:
                pass
            print(x,type(x))
            for j in range(1,4):
                try:
                    self.labelList[-j].config(text=self.data[-j][0])
                except IndexError:
                    pass
            if x>1:
                self.data.clear()
                for item in self.labelList:
                    item.config(text="")
            time.sleep(self.sleepTime)# 单位 s
            # 短延迟（< 100 毫秒）：用户通常不会感觉到延迟，界面看起来是流畅的。
            # 中等延迟（100-500 毫秒）：用户可能会感觉到轻微的延迟，但通常是可以接受的。
            # 长延迟（> 500 毫秒）：用户会明显感觉到延迟，可能会影响体验。




if __name__ == '__main__':
    url="https://github.com/Pfolg/MonitorKeyboard"
    config_file="MKConfig.json"
    config={
        "托盘名称/name":"MonitorKeyboard",
        "logo":".\\logo.ico",
        "描述/description":"monitoring your keyboard",
        "文本背景颜色/text_bg":"#870eb3",
        "文本前景颜色/text_fg":None,
        "字体/font":None,
        "是否加粗/bold?":True,
        "字号/text_size":24,
        "响应时间/time.sleep(?)":.05,
        "PS":"如果你懂Python，你可以自己改代码。If you understand Python, you can modify the code yourself."
    }
    if os.path.exists(config_file):
        with open(config_file,"r",encoding="utf-8") as file:
            config=json.load(file)
    else:
        with open(config_file,"w",encoding="utf-8") as file:
            json.dump(config,file,indent=4,ensure_ascii=False)
    # 防刁民？不存在的，懒得改，弄坏了电脑自己负责！Be sure your setting！
    your_font=config.get("字体/font")
    if not your_font:
        your_font=("ariblk.ttf bold", 24)
    else:
        if config.get("是否加粗/bold?"):
            your_font=your_font+" bold"
        elif config.get("字号/text_size"):
            your_font=(your_font,config.get("字号/text_size"))

    if not config.get("文本前景颜色/text_fg"):
        tfg="#ffffff"
    else:
        tfg=config.get("文本前景颜色/text_fg")
    app=MonitorKeyboard(
        name=config.get("托盘名称/name"),
        picture=config.get("logo"),
        description=config.get("描述/description"),
        text_bg=config.get("文本背景颜色/text_bg"),
        text_fg=tfg,
        font=your_font,
        sleepTime=config.get("响应时间/time.sleep(?)")
    )