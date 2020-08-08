from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QPixmap
import os, json

# from model import dataservice

class VideoCtrl:
    ctrl_label = None # 视频label控件
    note = ''

    now_count = 0 # 当前播放位置
    list_image = []

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
        self.videos_data = {} # { (0,1): VideoCtrl(), ... }
        rootdir = './data/fyc'
        list_video = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for i in range(len(list_video)):
            video_dir = os.path.join(rootdir, list_video[i])
            list_img = os.listdir(video_dir)
            key = (i // 3, i % 3)
            self.videos_data[key] = VideoCtrl()
            self.videos_data[key].note = list_video[i]
            self.videos_data[key].list_image = [] # 设置为空列表，否则可能读取上一个循环的list_image
            for j in range(len(list_img)):
                img_path = os.path.join(video_dir, list_img[j])
                self.videos_data[key].list_image.append(img_path)

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

    def getVideoCtrl(self):
        pass

    def setLabelFrame(self, target_label):
        # 设置边框样式 可选样式有Box Panel等
        target_label.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 只有加了这步才能设置边框颜色
        # 可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        target_label.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置线条宽度
        target_label.setLineWidth(2)
        # 设置背景颜色，包括边框颜色
        target_label.setStyleSheet('background-color: rgb(255, 0, 0)')

    def createSplitLine(self):
        split_label = QLabel()
        split_label.setFrameShape(QtWidgets.QFrame.Box)
        split_label.setMaximumHeight(2)
        return split_label

    def getCenterHBox(self, ctrl):
        note_hbox = QHBoxLayout()
        note_hbox.addStretch(1)
        note_hbox.addWidget(ctrl)
        note_hbox.addStretch(1)
        return note_hbox

    def initUI(self):
        self.initMenu()

        # 左边视频区-初始化数据
        self.grid_video = QGridLayout()
        self.positions = [(i, j) for i in range(3) for j in range(3)]
        for pos in self.positions:
            # 获取视频第一个图像
            first_img = self.videos_data[pos].list_image[0]
            self.videos_data[pos].ctrl_label = QLabel() # 创建label对象
            self.videos_data[pos].ctrl_label.setPixmap(QPixmap(first_img))
            self.setLabelFrame(self.videos_data[pos].ctrl_label) # 图片label设置边框

            # 获取水平居中标题布局
            note_label = QLabel(self.videos_data[pos].note)
            note_hbox = self.getCenterHBox(note_label)

            # 视频控件展示到网格
            video_box = QVBoxLayout()
            video_box.addWidget(self.videos_data[pos].ctrl_label) # 图片
            video_box.addLayout(note_hbox) # 文字
            video_box.addWidget(self.createSplitLine()) # 分割线

            self.grid_video.addLayout(video_box, *pos)

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
        self.timer.start(35) # 开启定时器40毫秒循环

    def showNextImage(self):
        # 控制每个视频，播放下一张图片
        for pos in self.positions:
            count = self.videos_data[pos].now_count
            list_img = self.videos_data[pos].list_image
            self.videos_data[pos].ctrl_label.setPixmap(QPixmap(list_img[count]))
            self.videos_data[pos].now_count += 1
            if self.videos_data[pos].now_count == len(list_img):
                self.videos_data[pos].now_count = 0

    def actFlashOnClick(self):
        print('actFlashOnClick')
        # self.browser.load(QUrl.fromLocalFile(self.url))
