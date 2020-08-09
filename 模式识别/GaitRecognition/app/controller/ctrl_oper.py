from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

class CtrlOper:
    # 给Label加边框
    def setLabelFrame(self, target_label, isOpen=True):
        if isOpen:
            # 设置边框样式 可选样式有Box Panel等
            target_label.setFrameShape(QtWidgets.QFrame.Box)
            # 设置阴影 只有加了这步才能设置边框颜色
            # 可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
            target_label.setFrameShadow(QtWidgets.QFrame.Raised)
            # 设置线条宽度
            target_label.setLineWidth(2)
            # 设置背景颜色，包括边框颜色
            target_label.setStyleSheet('background-color: rgb(255, 0, 0)')
        else:
            # 设置线条宽度
            target_label.setLineWidth(0)

    # 创建分割线
    def createSplitLine(self):
        split_label = QLabel()
        split_label.setFrameShape(QtWidgets.QFrame.Box)
        split_label.setMaximumHeight(2)
        return split_label

    # 创建控件水平居中布局
    def getCenterHBox(self, ctrl):
        note_hbox = QHBoxLayout()
        note_hbox.addStretch(1)
        note_hbox.addWidget(ctrl)
        note_hbox.addStretch(1)
        return note_hbox
