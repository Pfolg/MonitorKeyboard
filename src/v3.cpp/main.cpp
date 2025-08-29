#include <QApplication>
#include <QDebug>
#include "globalinputlistener.h"
#include "convertcodetostring.h"
#include "window.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    GlobalInputListener listener;
    Widget w;
    w.show();

    // 连接信号到槽函数
    // 键盘按键
    QObject::connect(&listener, &GlobalInputListener::keyReleased, [&](int keyCode, ModifierKeys modifiers)
                     {
                         QString keyName = keyCodeToKeyString(keyCode);
                         QString modifiersName = modifiersToString(modifiers);
                         qDebug() << "Key released:" << keyName << "Modifiers:" << modifiersName; 
                        w.on_keyRelease(keyName, modifiersName); });

    // 鼠标按键
    QObject::connect(&listener, &GlobalInputListener::mouseReleased, [&](MouseButton button, int x, int y, ModifierKeys modifiers)
                     {
                        //  QString buttonName=(button+" "+keyCodeToKeyString(button));
                         QString buttonName=mouseCodeToString(button);
                         QString modifiersName = modifiersToString(modifiers);
                         qDebug() << "Mouse button released:" << buttonName << "at (" << x << "," << y << ") Modifiers:" << modifiersName;
                         w.on_keyRelease(buttonName, modifiersName); });
    // 鼠标移动
    QObject::connect(&listener, &GlobalInputListener::mouseMoved, [&](int x, int y, ModifierKeys modifiers)
                     {
                         QString modifiersName = modifiersToString(modifiers);
                         qDebug() << "Mouse moved to (" << x << "," << y << ") "; 
                        w.on_mouseMove(x,y); });

    // 开始监听
    if (!listener.startListening())
    {
        qCritical() << "Failed to start global input listening";
        return 1;
    }

    qDebug() << "Global input listener is running. Press Ctrl+C to exit.";

    return a.exec();
}
