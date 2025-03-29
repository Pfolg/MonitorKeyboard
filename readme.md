### About
![alt text](./MonitorKeyboard/logo.ico)

A simple Program which is used to show which key you pressd.

### Function

Double click the `.exe` file to run it.

you can also clone the repo to set it yourself.

when you pressed a key, it will be shown in 1 seconds on your screen.

new：mouse&keyboard

~~old File struct:~~
~~~
---
-main.py
-logo.ico (must)
-requirements.txt
-MKConfig.json
-readme.md
-license
~~~

new File struct:
~~~
---
-*.ico
-user_set.json
-*.py
...
~~~
### Infor
old: you can watch my video to know more: https://www.bilibili.com/video/BV1Vhw9euEqa/

we haven't make video about the new version.

![alt text](/asset/image.png)

**~~Old MKConfig.json~~**
~~~json
{
    "托盘名称/name": "MonitorKeyboard",
    "logo": ".\\logo.ico",
    "描述/description": "monitoring your keyboard",
    "文本背景颜色/text_bg": "#870eb3",
    "文本前景颜色/text_fg": null,
    "字体/font": null,
    "是否加粗/bold?": true,
    "字号/text_size": 24,
    "响应时间/time.sleep(?)": 0.05,
    "PS": "如果你懂Python，你可以自己改代码。If you understand Python, you can modify the code yourself."
}
~~~ 
![alt text](/asset/image-1.png)

![alt text](/asset/image-2.png)

**New Set**

define it by your-self:
~~~json
{
    "logo": "input-keyboard.ico",
    "name": "Keyboard Monitor",
    "description": "monitoring your keyboard",
    "font": "Ubuntu Mono",
    "bold": true,
    "foreground": "rgba(255, 255, 255, .8)",
    "background": "rgba(148, 255, 245, .6)",
    "geometry": [
        60,
        500,
        300,
        200
    ],
    "fontSize1": 24,
    "fontSize2": 10,
    "looptime": 0.05,
    "show_mouse_location": true,
    "show_time": 1
}
~~~

### Verson 1.0.0
preview:

![alt text](/asset/image3.png)
 
![alt text](/asset/image4.png)

### Last but not least
Thanks every package's Contributors！

Feel free to make Issue and PR!