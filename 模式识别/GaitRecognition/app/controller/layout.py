from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
import os, json

from controller import ctrl_oper
from controller import result_dialog
from model import gait_view
from model import match_algo

DEFAULT_IMG = './data/target.png'
TIME_SPACE = 5

class ImageInfo:
    def __init__(self, img_path):
        self.path = img_path
        width = 0

class VideoCtrl:
    ctrl_label = None # 视频label控件
    note = ''
    note_label = None

    now_count = 0 # 当前播放位置
    list_image = []

class MainLayout(QMainWindow):
    coper = ctrl_oper.CtrlOper()
    malgo = match_algo.MatchAlgo()
    startSearch = False
    timeSpace = 1

    def __init__(self):
        super(MainLayout, self).__init__()
        self.setWindowTitle("监控寻人系统 [v0.1]")
        self.resize(1300, 810)
        self.timer = QTimer()

        self.initData()
        self.initUI()
        self.connSlot()
        self.startTimer(30)

    def initData(self):
        # 读取数据-视频文件夹
        self.videos_data = {} # { (0,1): VideoCtrl(), ... }
        rootdir = './data/video'
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
                self.videos_data[key].list_image.append(ImageInfo(img_path))

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

        """左边视频区-初始化数据"""
        self.grid_video = QGridLayout()
        self.positions = [(i, j) for i in range(3) for j in range(3)]
        for pos in self.positions:
            # 获取视频第一个图像
            first_img = self.videos_data[pos].list_image[0].path
            self.videos_data[pos].ctrl_label = QLabel() # 创建label对象
            self.videos_data[pos].ctrl_label.setPixmap(QPixmap(first_img))

            # 获取水平居中标题布局
            self.videos_data[pos].note_label = QLabel(self.videos_data[pos].note)
            note_hbox = self.coper.getCenterHBox(self.videos_data[pos].note_label)

            # 视频控件展示到网格
            video_box = QVBoxLayout()
            video_box.addWidget(self.videos_data[pos].ctrl_label) # 图片
            video_box.addLayout(note_hbox) # 文字
            video_box.addWidget(self.coper.createSplitLine()) # 分割线

            self.grid_video.addLayout(video_box, *pos)

        """右边操作面板"""
        self.panel = QVBoxLayout()

        # 标题
        self.title_label = QLabel("查找人物")
        self.title_label.resize(300, 30)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color:rgb(10,10,10,255);font-size:25px;font-weight:bold;font-family:Roman times;")

        # 初始图片
        self.people = QLabel(self)
        self.people.setPixmap(QPixmap(DEFAULT_IMG))

        # 文本搜索
        self.input_edit = QLineEdit('45_2')
        self.formLayout = QFormLayout()
        self.formLayout.addRow('高亮视频', self.input_edit)

        # 图片选择
        self.filePathEdit = QLineEdit(DEFAULT_IMG)
        self.btnSelect = QPushButton("选择文件")
        self.btnSelect.setMaximumHeight(22)
        self.file_hbox = QHBoxLayout()
        self.file_hbox.addWidget(self.filePathEdit)
        self.file_hbox.addWidget(self.btnSelect)

        # 查找按钮
        self.init_button = QPushButton('初始化')
        self.search_button = QPushButton('查找')

        # 元素放置到操作面板
        self.panel.addWidget(self.title_label, 2)
        self.panel.addWidget(self.people, 4)
        self.panel.addLayout(self.formLayout, 1)
        self.panel.addLayout(self.file_hbox, 1)
        self.panel.addWidget(self.init_button, 1)
        self.panel.addWidget(self.search_button, 1)
        self.panel.addWidget(QLabel(), 3)

        """应用布局"""
        hbox = QHBoxLayout()
        hbox.addLayout(self.grid_video, 3)
        hbox.addLayout(self.panel, 1)

        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)

    def connSlot(self):
        # 刷新页面
        # self.actFlash.triggered.connect(self.actFlashOnClick)
        # 初始化视频
        self.init_button.clicked.connect(self.btnInitOnClick)
        # 查找视频
        self.search_button.clicked.connect(self.btnSearchPeopleOnClick)
        # 选择文件
        self.btnSelect.clicked.connect(self.btnSelectOnClick)
        # 定时器事件处理
        self.timer.timeout.connect(self.showNextImage)

    # 创建定时器并开启
    def startTimer(self, lenTime):
        for pos in self.positions:
            # 取消高亮边框
            self.coper.setLabelFrame(self.videos_data[pos].ctrl_label, False)
        self.timer.start(lenTime) # 开启定时器40毫秒循环

    def stopTimer(self):
        self.timer.stop()

    # 定时刷新视频
    def showNextImage(self):
        # 控制每个视频，播放下一张图片
        for pos in self.positions:
            count = self.videos_data[pos].now_count
            list_img = self.videos_data[pos].list_image

            # 调用匹配算法
            result = match_algo.CompareResult()
            if self.startSearch and self.malgo.isImageSame(list_img[count].path, self.filePathEdit.text(), result):
                self.coper.setLabelFrame(self.videos_data[pos].ctrl_label, True) # 视频label设置边框
                self.stopTimer()
                show_box = result_dialog.ResultDialog(list_img[count].path, self.filePathEdit.text(), result)
                show_box.exec_()
            note = self.videos_data[pos].note
            self.videos_data[pos].note_label.setText('%s [%d, %d]' % (note, result.area_diff, result.height_diff))

            # 继续扫描
            self.videos_data[pos].ctrl_label.setPixmap(QPixmap(list_img[count].path))
            self.videos_data[pos].now_count += self.timeSpace
            if self.videos_data[pos].now_count >= len(list_img):
                self.videos_data[pos].now_count = 0

    def actFlashOnClick(self):
        print('actFlashOnClick')
        # self.browser.load(QUrl.fromLocalFile(self.url))

    # 初始化视频
    def btnInitOnClick(self):
        print('btnInitOnClick')

        for pos in self.positions:
            list_img = self.videos_data[pos].list_image
            i = 0
            end = len(list_img)
            for img in list_img:
                i += 1
                print('[%d/%d] %s' % (i, end, self.videos_data[pos].note))
                img.width = gait_view.GR_GetStepLength(img.path)

        QMessageBox.information(self, "提示", "初始化成功！")


    # 查找视频
    def btnSearchPeopleOnClick(self):
        print('btnSearchPeopleOnClick')
        self.startSearch = True
        self.timeSpace = TIME_SPACE
        self.startTimer(1)

    # 选择图片
    def btnSelectOnClick(self):
        select_filepath, ok = QFileDialog.getOpenFileName(self, "打开图片",
                                                        ".", # 默认当前路径
                                                        "png Files (*.png);;jpg Files (*.jpg);;All Files (*)")
        if ok:
            self.filePathEdit.setText(str(select_filepath))
            self.people.setPixmap(QPixmap(str(select_filepath)))
        else:
            QMessageBox.warning(self, "警告", "选择的文件失败，请重试")
            return False
