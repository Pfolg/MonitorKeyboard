# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME KeyboardMonitor
AUTHOR Pfolg
TIME 2025/3/28 22:25
"""
import json
import os.path
import sys
import threading
import time
from datetime import datetime

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QLabel, QMessageBox
from pynput import keyboard, mouse


def struct_time_to_datetime(st):
    """
    将 struct_time 转换为 datetime 对象。
    """
    return datetime.fromtimestamp(time.mktime(st))


class MyQWidget(QWidget):
    def __init__(self):
        super().__init__()

    # 忽略关闭事件
    def closeEvent(self, event):
        event.ignore()


def write_setting(setting: dict = None):
    if not setting:
        setting = {
            "logo": "input-keyboard.ico",
            "name": "Keyboard Monitor",
            "description": "monitoring your keyboard",
            "font": "Ubuntu Mono",
            "bold": True,
            "foreground": "rgba(255, 255, 255, .8)",
            "background": "rgba(148, 255, 245, .6)",
            "geometry": [60, 500, 300, 200],
            "fontSize1": 24,
            "fontSize2": 10,
            "looptime": .05,
            "show_mouse_location": True,
            "show_time": 1,
        }
    with open("user_set.json", "w", encoding="utf-8") as file:
        json.dump(setting, file, indent=4, ensure_ascii=False)


def read_setting():
    if not os.path.exists("user_set.json"):
        write_setting()
        return
    else:
        with open("user_set.json", "r", encoding="utf-8") as file:
            user_set: dict = json.load(file)
            if user_set:
                return user_set


class MyApp:
    def __init__(self):
        # 定义参数
        self.logo = "input-keyboard.ico"  # 托盘图标
        self.name = "Keyboard Monitor"  # 应用名称
        self.description = "monitoring your keyboard"  # 描述
        self.font = "Ubuntu Mono"  # 字体
        self.bold = True  # 加粗
        self.foreground = "rgba(255, 255, 255, .8)"  # 前景颜色
        self.background = "rgba(148, 255, 245, .6)"  # 背景
        self.geometry = [60, 500, 300, 200]  # 窗口位置
        self.fontSize1 = 24  # 字体大小
        self.fontSize2 = 10
        self.looptime = 0.05  # 循环间隔
        self.show_mouse_location = True  # 展示鼠标位置
        self.show_time = 1  # 展示时间
        # 读取设置
        self.read_set()
        print(
            f"""Your config is
    tray logo >>> {self.logo}
    tray name >>> {self.name}
    tray description >>> {self.description}
    label font >>> {self.font}, {self.fontSize1}&{self.fontSize2}, bold={self.bold}
    font foreground >>> {self.foreground}
    font background >>> {self.background}
    window geometry >>> x={self.geometry[0]}, y={self.geometry[1]}, width={self.geometry[2]}, height={self.geometry[3]}
    loop time >>> {self.looptime * 1000} ms
    show mouse location >>> {self.show_mouse_location}
    show time >>> {self.show_time}
            """
        )
        # 设定窗口
        self.root = MyQWidget()
        # 设定托盘
        self.tray = QSystemTrayIcon()

        # 设定标签
        self.labels = [QLabel() for _ in range(3)]
        self.mouse_location = QLabel()
        self.data = []
        self.current_position = (0, 0)  # 记录当前鼠标坐标
        self.keyboardListener = keyboard.Listener(on_press=self.on_key_press, )
        self.mouseListener = mouse.Listener(on_click=self.on_mouse_click, on_scroll=self.on_mouse_scroll,
                                            on_move=self.on_mouse_move)
        self.setRoot()
        self.setTray()
        self.root.show()
        self.tray.show()
        self.keyboardListener.start()
        self.mouseListener.start()
        threading.Thread(target=self.manage_data, daemon=True).start()

    # 读取设置
    def read_set(self):
        data = read_setting()
        if data:
            if data.get("logo"):
                self.logo = data.get("logo")  # 托盘图标
            if data.get("name"):
                self.name = data.get("name")  # 应用名称
            if data.get("description"):
                self.description = data.get("description")  # 描述
            if data.get("font"):
                self.font = data.get("font")  # 字体
            if data.get("bold"):
                self.bold = True  # 加粗
            else:
                self.bold = False
            if data.get("foreground"):
                self.foreground = data.get("foreground")  # 前景颜色
            if data.get("background"):
                self.background = "rgba(148, 255, 245, .6)"  # 背景
            if data.get("geometry"):
                self.geometry = data.get("geometry")  # 窗口位置
            if data.get("fontSize1"):
                self.fontSize1 = data.get("fontSize1")  # 字体大小
            if data.get("fontSize2"):
                self.fontSize2 = data.get("fontSize2")
            if data.get("looptime"):
                self.looptime = data.get("looptime")  # 循环间隔
            if data.get("show_mouse_location"):
                self.show_mouse_location = True  # 展示鼠标位置
            else:
                self.show_mouse_location = False
            if data.get("show_time"):
                self.show_time = 1  # 展示时间
        else:
            QMessageBox.warning(None, "Warning", "Your setting seemly empty!\nUse default setting.")

    # 数据管理
    def manage_data(self):
        # 计时器，获取输入时刷新，没有输入等待一定时间后清除相应数据->记录日志
        while True:
            x = 0
            try:
                mid_t = str(
                    struct_time_to_datetime(time.localtime()) - struct_time_to_datetime(self.data[-1][1])).split(":")
                for i in mid_t:
                    x += int(i)
            except IndexError:
                pass
            # print(x,type(x))
            for j in range(1, 4):
                try:
                    text = self.data[-j][0]
                    if text:
                        self.labels[-j].setText(text)
                        self.labels[-j].setVisible(True)
                except IndexError:
                    pass
            if x > self.show_time:
                # # 记录日志
                # if self.write_log:
                #     with open(log_file, "a", encoding="utf-8") as log:
                #         log.write("{}\t{}\n".format(len(self.data), self.data))
                # 清除数据
                self.data.clear()
                for item in [*self.labels, self.mouse_location]:
                    item.setVisible(False)
            time.sleep(self.looptime)  # 单位 s
            # 短延迟（< 100 毫秒）：用户通常不会感觉到延迟，界面看起来是流畅的。
            # 中等延迟（100-500 毫秒）：用户可能会感觉到轻微的延迟，但通常是可以接受的。
            # 长延迟（> 500 毫秒）：用户会明显感觉到延迟，可能会影响体验。

    # 鼠标移动事件回调
    def on_mouse_move(self, x, y):
        """实时获取鼠标坐标"""
        # self.current_position = (x, y)
        self.mouse_location.setText(f"X:{x}, Y:{y}")
        self.mouse_location.setVisible(self.show_mouse_location)
        self.data.append([None, time.localtime()])

    # 按钮按下
    def on_key_press(self, key):
        """处理键盘按下事件"""
        # 处理数字小键盘（通过虚拟键码判断）
        if hasattr(key, 'vk'):
            if 96 <= key.vk <= 105:  # 小键盘 0-9
                key_char = str(key.vk - 96)  # 转换为字符
                self.data.append([key_char, time.localtime()])
                print(self.data[-1])
                return
        try:
            # 处理普通按键
            key_name = key.char
        except AttributeError:
            # 处理特殊按键
            key_name = key.name.replace('_', ' ').title()
        except NotImplementedError:
            print("Have an error but ignored")
            key_name = None

        try:
            if len(key_name) == 1:
                key_name = key_name.upper()
        except TypeError:
            pass
        self.data.append([key_name, time.localtime()])
        print(self.data[-1])

    # 鼠标按钮
    def on_mouse_click(self, x, y, button, pressed):
        """处理鼠标点击事件"""
        button_name = "Mouse " + button.name.title()  # 转换为首字母大写

        if pressed:
            self.data.append([button_name, time.localtime()])
            print(self.data[-1])

    # 鼠标滚动
    def on_mouse_scroll(self, x, y, dx, dy):
        direction = None
        if dy > 0:  # 垂直向上滚动
            direction = "Wheel Up"
        elif dy < 0:  # 垂直向下滚动
            direction = "Wheel Down"
        if dx != 0:  # 处理水平滚动（如有）
            if dx > 0:
                direction = "Wheel Right"
            else:
                direction = "Wheel Left"

        if direction:
            self.data.append([direction, time.localtime()])
            print(self.data[-1])

    def setTray(self):
        # 设置托盘
        self.tray.setParent(None)
        self.tray.setIcon(QIcon(self.logo))
        self.tray.setToolTip(self.description)
        self.tray.setObjectName(self.name)
        # 设置菜单
        menu = QMenu()
        quitApp = QAction(parent=menu)
        quitApp.setText("Quit")
        quitApp.triggered.connect(sys.exit)

        menu.addActions([quitApp])

        self.tray.setContextMenu(menu)

    def setRoot(self):
        self.root.setParent(None)
        self.root.setGeometry(*self.geometry)
        # 设定字体
        font = QtGui.QFont()
        font.setFamily(self.font)
        font.setPointSize(self.fontSize1)
        font.setBold(self.bold)
        # 设定标签
        x, y = 50, 0
        for label in self.labels:
            label.setParent(self.root)
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label.setFont(font)
            label.setGeometry(x, y, 250, 50)
            label.setVisible(False)
            label.setText("初始化中")
            label.setStyleSheet(
                f"""
                color: {self.foreground};
                background-color: {self.background};
                """
            )
            y += 60
        # 鼠标位置标签设定
        self.mouse_location.setParent(self.root)
        self.mouse_location.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mouse_location.setGeometry(50, 180, 120, 20)
        self.mouse_location.setStyleSheet(
            f"""
                color: {self.foreground};
                background-color: {self.background};
                """
        )
        self.mouse_location.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font.setPointSize(self.fontSize2)
        self.mouse_location.setFont(font)
        self.mouse_location.setText("X:9999, Y:9999")
        self.mouse_location.setVisible(False)
        # 启用透明度
        self.root.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # 窗口顶置，去标题栏，去除任务栏图标，鼠标穿透
        self.root.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyApp = MyApp()
    sys.exit(app.exec())
