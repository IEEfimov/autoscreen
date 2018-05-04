import pyautogui as gui
import time
import screen
import sys
import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QColor, QPainter
from PyQt5.QtWidgets import (QWidget,
                             QPushButton, QApplication, QFileDialog, QLabel)


class MainWindow(QWidget):

    selected = 0
    regs = [(0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0)]
    x = 0
    y = 0
    width = 0
    height = 0
    isPressed = False
    qp = QPainter

    def __init__(self, w, h):
        super().__init__()
        oImage = QImage("resource/FullScreen.png")
        sImage = oImage.scaled(QSize(w, h))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.load_regions()
        self.setPalette(palette)
        self.setWindowTitle("ooops! It's just a screenshot!")

        self.showFullScreen()
        self.initUI()

    def save_regions(self):
        s = open('resource/save.conf', 'w')
        try:
            for index in self.regs:
                for i in index:
                    s.write(str(i) + '\n')

        except Exception:
            print("trouble with save")

    def load_regions(self):
        try:
            s = open('resource/save.conf', 'r')
            l = [line.strip() for line in s]
            print(l)
            for i in range(0, 3):
                temp = [0, 1, 2, 3]
                for j in range(0, 4):
                    num = (int(l[i * 4 + j]))
                    temp[j] = num
                self.regs[i] = (temp[0], temp[1], temp[2], temp[3])
            s.close()
        except Exception:
            print("some trouble with load regions, as u can see")
        pass

    def mousePressEvent(self, QMouseEvent):
        self.x = QMouseEvent.pos().x()
        self.y = QMouseEvent.pos().y()
        self.isPressed = True

    def mouseMoveEvent(self, e):
        if self.isPressed:
            self.width = int(e.x() - self.x)
            self.height = int(e.y() - self.y)
            self.repaint()

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        if self.width < 0:
            self.width = abs(self.width)
            self.x = self.x - self.width
        if self.height < 0:
            self.height = abs(self.height)
            self.y = self.y - self.height
        self.regs[self.selected] = (self.x, self.y, self.width, self.height)
        self.height = 0
        self.width = 0

    def keyPressEvent(self, e):
        pass
        if str(e.nativeScanCode == '1'):
            self.close()

    def btnR_click(self):
        self.selected = 0
        self.repaint()

    def btnG_click(self):
        self.selected = 1
        self.repaint()

    def btnB_click(self):
        self.selected = 2
        self.repaint()

    def start_click(self):
        gui.hotkey('alt', 'tab')
        time.sleep(1)
        self.save_regions()
        screen.doMagic(self.regs)

    def paintEvent(self, e):
        self.qp = QPainter()
        self.qp.begin(self)
        self.drawRectangles(self.qp)
        self.qp.end()

    def drawRectangles(self, qp):
        col1 = QColor(0, 0, 0)
        col1.setNamedColor('#d4d4d4')
        col1.setAlpha(120)
        col2 = QColor(100, 25, 25)
        for i in range(0, 3):
            if i == 0:
                col2.setRgb(100, 0, 0, 120)
            elif i == 1:
                col2.setRgb(0, 100, 50, 120)
            elif i == 2:
                col2.setRgb(0, 50, 100, 120)
            if self.selected == i:
                col2.setAlpha(50)

            qp.setPen(col1)
            qp.setBrush(col2)
            qp.drawRect(self.regs[i][0], self.regs[i][1], self.regs[i][2], self.regs[i][3])

        if self.selected == 0:
            col2.setRgb(100, 0, 0, 120)
        elif self.selected == 1:
            col2.setRgb(0, 100, 50, 120)
        elif self.selected == 2:
            col2.setRgb(0, 50, 100, 120)
        col1 = QColor(0, 0, 0)
        col1.setNamedColor('#d4d4d4')
        col1.setAlpha(120)
        qp.setPen(col1)

        col2.setAlpha(120)
        qp.setBrush(col2)
        qp.drawRect(self.x, self.y, self.width, self.height)

    def initUI(self):

        self.setMouseTracking(True)
        self.btnR = QPushButton('R', self)
        self.btnR.move(1000, 120)
        self.btnR.clicked.connect(self.btnR_click)
        self.btnR.setVisible(True)

        self.btnG = QPushButton('G', self)
        self.btnG.move(1000, 150)
        self.btnG.clicked.connect(self.btnG_click)
        self.btnG.setVisible(True)

        self.btnB = QPushButton('B', self)
        self.btnB.move(1000, 180)
        self.btnB.clicked.connect(self.btnB_click)
        self.btnB.setVisible(True)

        self.btnStart = QPushButton('Сделать магию!', self)
        self.btnStart.move(1000, 350)
        self.btnStart.clicked.connect(self.start_click)
        self.btnStart.setVisible(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    w = screen_resolution.width()
    h = screen_resolution.height()
    gui.hotkey('alt', 'tab')

    time.sleep(0.2)
    scr = gui.screenshot(region=(0, 0, w, h))
    scr.save("resource/FullScreen.png")

    ex = MainWindow(w, h)
    sys.exit(app.exec_())

