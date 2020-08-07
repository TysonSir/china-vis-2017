from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QPixmap
import os, json

# from model import dataservice

class VideoCtrl:
    ctrl_label = None # 视频label控件
    now_count = 0 # 当前播放位置

class MainLayout(QMainWindow):

    def __init__(self):
        super(MainLayout, self).__init__()
        self.setWindowTitle("监控寻人系统 [v0.1]")
        self.resize(1300, 810)

        self.initData()
        self.initUI()
        self.connSlot()
        self.startTimer()

    def initData(self):
        # 读取数据-视频文件夹
        self.videos_path = {} # { (0,1): ['./1.png', './2.png'], ... }
        rootdir = './data/001'
        list_video = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for i in range(len(list_video)):
            video_dir = os.path.join(rootdir, list_video[i])
            list_img = os.listdir(video_dir)
            key = (i // 3, i % 3)
            self.videos_path[key] = []
            for j in range(len(list_img)):
                img_path = os.path.join(video_dir, list_img[j])
                self.videos_path[key].append(img_path)

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

        # 左边视频区-初始化数据
        self.videos_play = {} # { (0,1): VideoCtrl(), ... }
        self.grid_video = QGridLayout()
        self.positions = [(i, j) for i in range(3) for j in range(3)]
        for pos in self.positions:
            vc = VideoCtrl()
            vc.ctrl_label = QLabel(self)
            first_img = self.videos_path[pos][0]
            vc.ctrl_label.setPixmap(QPixmap(first_img))
            self.grid_video.addWidget(vc.ctrl_label, *pos)
            vc.now_count = 0
            self.videos_play[pos] = vc # 保存9个视频数据

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

    def startTimer(self):
        # 创建定时器并开启
        self.timer = QTimer()
        self.timer.timeout.connect(self.showNextImage)
        self.timer.start(40) # 开启定时器40毫秒循环

    def showNextImage(self):
        # 控制每个视频，播放下一张图片
        for pos in self.positions:
            count = self.videos_play[pos].now_count
            list_img = self.videos_path[pos]
            self.videos_play[pos].ctrl_label.setPixmap(QPixmap(list_img[count]))
            self.videos_play[pos].now_count += 1
            if self.videos_play[pos].now_count == len(list_img):
                self.videos_play[pos].now_count = 0

    def actFlashOnClick(self):
        print('actFlashOnClick')
        # self.browser.load(QUrl.fromLocalFile(self.url))
