#include "window.h"
#include <QMessageBox>
#include <QDebug>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    QCoreApplication *coreapp = QCoreApplication::instance();
    QApplication *app = qobject_cast<QApplication *>(coreapp);
    QScreen *screen = app->primaryScreen();
    this->setGeometry(0, 0, screen->geometry().width(), screen->geometry().height());

    // 窗口顶置，去标题栏，去除任务栏图标，鼠标穿透，窗口透明，不可聚焦
    this->setAttribute(Qt::WA_TranslucentBackground, true);
    this->setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint | Qt::ToolTip | Qt::WindowTransparentForInput | Qt::WindowDoesNotAcceptFocus);
    this->keyLabel = new QLabel(this);
    this->mouseLabel = new QLabel(this);
    // 样式
    QString style = "background-color: rgba(37, 153, 236, 0.86); color: rgba(255, 255, 255, 0.8);";
    keyLabel->setStyleSheet(style);
    mouseLabel->setStyleSheet(style);
    keyLabel->setAlignment(Qt::AlignCenter);
    mouseLabel->setAlignment(Qt::AlignCenter);
    QFont font("Maple Mono NF CN", 24, 100);
    font.setBold(true);
    // font.setItalic(true);
    keyLabel->setFont(font);
    mouseLabel->setFont(font);
    keyLabel->hide();
    mouseLabel->hide();
    this->adjustLabel();

    fadeTimer1 = new QTimer(this);
    fadeTimer2 = new QTimer(this);
    connect(fadeTimer1, &QTimer::timeout, this, [this]()
            { keyLabel->hide(); });
    connect(fadeTimer2, &QTimer::timeout, this, [this]()
            { mouseLabel->hide(); });

    this->checkSingleInstance(16658);
}

void Widget::on_keyRelease(QString keyName, QString modifiersName)
{
    if (keyName.isEmpty())
    {
        this->keyLabel->setText(modifiersName);
    }
    else if (modifiersName.isEmpty())
    {
        this->keyLabel->setText(keyName);
    }
    else
    {
        this->keyLabel->setText(modifiersName + " " + keyName);
    }
    if (fadeTimer1->isActive())
    {
        fadeTimer1->stop();
    }
    this->keyLabel->show();
    fadeTimer1->start(3000);
}
void Widget::on_mouseMove(int x, int y)
{
    this->mouseLabel->setText("(" + QString::number(x) + "," + QString::number(y) + ")");
    if (fadeTimer2->isActive())
    {
        fadeTimer2->stop();
    }
    mouseLabel->show();
    fadeTimer2->start(1000);
}

Widget::~Widget()
{
}
void Widget::adjustLabel(int up, int down, int left, int right)
{
    // 清除现有布局
    if (this->layout())
    {
        delete this->layout();
    }

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    // 上方空白 (拉伸因子 = up)
    mainLayout->addStretch(up);

    // 水平布局容器
    QHBoxLayout *hContainer = new QHBoxLayout();
    // 左侧空白 (拉伸因子 = left)
    hContainer->addStretch(left);

    // 文字容器
    QVBoxLayout *textLayout = new QVBoxLayout();
    textLayout->addWidget(keyLabel);
    textLayout->addWidget(mouseLabel);
    hContainer->addLayout(textLayout);

    // 右侧空白 (拉伸因子 = right)
    hContainer->addStretch(right);

    // 添加水平容器到主布局
    mainLayout->addLayout(hContainer);

    // 下方空白 (拉伸因子 = down)
    mainLayout->addStretch(down);

    this->setLayout(mainLayout);
}

void Widget::closeEvent(QCloseEvent *event)
{
    event->ignore();
}

void Widget::checkSingleInstance(int port)
{
    QTcpSocket *singleInstanceSocket = new QTcpSocket(this);
    singleInstanceSocket->connectToHost("127.0.0.1", port);
    if (singleInstanceSocket->waitForConnected(100))
    {
        QMessageBox::warning(nullptr, "Warning", "端口 " + QString::number(port) + " 正在使用，可能已经有实例在运行，或者更改端口。");
        exit(0);
    }
    else
    {
        QTcpServer *server = new QTcpServer(this);
        if (!server->listen(QHostAddress::LocalHost, port))
        {
            QMessageBox::critical(nullptr, "Error", "无法监听端口 " + QString::number(port));
            exit(0);
        }
    }
}