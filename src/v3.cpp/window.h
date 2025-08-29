#ifndef WINDOW_H
#define WINDOW_H

#include <QCoreApplication>
#include <QWidget>
#include <QApplication>
#include <QScreen>
#include <QLabel>
#include <QVBoxLayout>
#include <QCloseEvent>
#include <QtNetwork/QTcpSocket>
#include <QtNetwork/QTcpServer>
#include <QString>
#include <QTimer>

QT_BEGIN_NAMESPACE
namespace Ui
{
    class Widget;
}
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();
    QLabel *keyLabel;
    QLabel *mouseLabel;
    QTimer *fadeTimer1;
    QTimer *fadeTimer2;
    void adjustLabel(int up = 7, int down = 1, int left = 1, int right = 1);
    void closeEvent(QCloseEvent *event);
    void checkSingleInstance(int port);
    void on_keyRelease(QString keyName, QString modifiersName);
    void on_mouseMove(int x, int y);

public slots:
};
#endif // WIDGET_H
