from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QPixmap
import os, json

# from model import dataservice

class MainLayout(QMainWindow):

    def __init__(self):
        super(MainLayout, self).__init__()
        self.setWindowTitle("监控寻人系统 [v0.1]")
        self.resize(1300, 810)

        self.initUI()
        self.initData()
        self.connSlot()

    def initData(self):
        pass

    def initMenu(self):
        # 创建Action
        self.actFlash = QAction("刷新")

        # 菜单栏
        # bar = self.menuBar()  # 获取菜单栏
        # edit = bar.addMenu("编辑")
        # edit.addAction(self.actFlash)

        #工具栏
        tool = self.addToolBar("Tool")
        tool.addAction(self.actFlash)
        tool.setToolButtonStyle(Qt.ToolButtonTextOnly)

    def initUI(self):
        self.initMenu()

        # 左边视频区
        self.grid_video = QGridLayout()
        positions = [(i, j) for i in range(3) for j in range(3)]
        for pos in positions:
            video = QLabel(self)
            video.setPixmap(QPixmap("./data/fn00/057.png"))
            self.grid_video.addWidget(video, *pos)

        # 右边操作面板
        self.panel = QVBoxLayout()
        self.people = QLabel(self)
        self.people.setText("测试员")
        self.panel.addWidget(self.people)

        # 应用布局
        hbox = QHBoxLayout()
        hbox.addLayout(self.grid_video, 3)
        hbox.addLayout(self.panel, 1)

        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)

    def connSlot(self):
        # 刷新页面
        # self.actFlash.triggered.connect(self.actFlashOnClick)
        pass

    def actFlashOnClick(self):
        print('actFlashOnClick')
        # self.browser.load(QUrl.fromLocalFile(self.url))
