#ifndef CONVERTCODETOSTRING_H
#define CONVERTCODETOSTRING_H
#include <QCoreApplication>
#include <QDebug>
#include <QKeySequence>
#include "globalinputlistener.h"
#include <QObject>

QString keyCodeToKeyString(int keyCode);
QString modifiersToString(ModifierKeys modifiers);
QString mouseCodeToString(MouseButton &button);
#endif // CONVERTCODETOSTRING_H