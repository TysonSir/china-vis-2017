from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel, QLineEdit, QTextEdit, QComboBox, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from controller import ctrl_oper

class ResultDialog(QDialog):
    coper = ctrl_oper.CtrlOper()

    def __init__(self, img1, img2):
        super(ResultDialog, self).__init__()
        self.setWindowTitle("对比")
        self.resize(750, 330)

        self.img1_path = img1
        self.img2_path = img2
        self.initUI()
        self.connSlot()

    def initUI(self):
        # 布局信息
        dstImgLabel = QLabel()
        dstNoteLabel = QLabel('视频')
        dstImgLabel.setPixmap(QPixmap(self.img2_path))

        srcImgLabel = QLabel()
        srcNoteLabel = QLabel('查找人物')
        srcImgLabel.setPixmap(QPixmap(self.img1_path))

        compare_hbox = QHBoxLayout()
        compare_hbox.addLayout(self.getImgHBox(dstImgLabel, self.coper.getCenterHBox(dstNoteLabel)))
        compare_hbox.addLayout(self.getImgHBox(srcImgLabel, self.coper.getCenterHBox(srcNoteLabel)))

        self.setLayout(compare_hbox)

    def connSlot(self):
        # self.btnAdd.clicked.connect(self.btnAddOnClick)
        pass

    def getImgHBox(self, imgLabel, note):
        img_box = QVBoxLayout()
        img_box.addWidget(imgLabel)
        img_box.addLayout(note)
        return img_box
