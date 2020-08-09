from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import os, json

from controller import ctrl_oper

class VideoCtrl:
    ctrl_label = None # 视频label控件
    note = ''

    now_count = 0 # 当前播放位置
    list_image = []

class MainLayout(QMainWindow):
    coper = ctrl_oper.CtrlOper()

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

    def initUI(self):
        self.initMenu()

        """左边视频区-初始化数据"""
        self.grid_video = QGridLayout()
        self.positions = [(i, j) for i in range(3) for j in range(3)]
        for pos in self.positions:
            # 获取视频第一个图像
            first_img = self.videos_data[pos].list_image[0]
            self.videos_data[pos].ctrl_label = QLabel() # 创建label对象
            self.videos_data[pos].ctrl_label.setPixmap(QPixmap(first_img))

            # 获取水平居中标题布局
            note_label = QLabel(self.videos_data[pos].note)
            note_hbox = self.coper.getCenterHBox(note_label)

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
        self.people.setPixmap(QPixmap('./data/fyc/45_2/fyc-45_2-026.png'))

        # 文本搜索
        self.input_edit = QLineEdit('45_2')
        self.formLayout = QFormLayout()
        self.formLayout.addRow('高亮视频', self.input_edit)

        # 图片选择
        self.filePathEdit = QLineEdit()
        self.btnSelect = QPushButton("选择文件")
        self.btnSelect.setMaximumHeight(22)
        self.file_hbox = QHBoxLayout()
        self.file_hbox.addWidget(self.filePathEdit)
        self.file_hbox.addWidget(self.btnSelect)

        # 查找按钮
        self.search_button = QPushButton('查找')

        # 元素放置到操作面板
        self.panel.addWidget(self.title_label, 2)
        self.panel.addWidget(self.people, 4)
        self.panel.addLayout(self.formLayout, 1)
        self.panel.addLayout(self.file_hbox, 1)
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
        # 查找视频
        self.search_button.clicked.connect(self.btnSearchPeopleOnClick)
        # 选择文件
        self.btnSelect.clicked.connect(self.btnSelectOnClick)

    # 创建定时器并开启
    def startTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.showNextImage)
        self.timer.start(35) # 开启定时器40毫秒循环

    # 定时刷新视频
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

    # 查找视频
    def btnSearchPeopleOnClick(self):
        print('btnSearchPeopleOnClick')
        for pos, video in self.videos_data.items():
            if video.note == self.input_edit.text():
                self.coper.setLabelFrame(video.ctrl_label, True) # 视频label设置边框
            else:
                # self.setLabelFrame(video.ctrl_label, False) # 视频label消除边框
                pass

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
