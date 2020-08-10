from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel, QLineEdit, QTextEdit, QComboBox, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import os, shutil

from controller import ctrl_oper
from model import gait_view

class ResultDialog(QDialog):
    coper = ctrl_oper.CtrlOper()

    def __init__(self, img1, img2):
        super(ResultDialog, self).__init__()
        self.setWindowTitle("对比")
        self.resize(750, 330)
        op_img1_path = './runtime/img1_%s' % os.path.basename(img1)
        shutil.copyfile(img1, op_img1_path)
        op_img2_path = './runtime/img2_%s' % os.path.basename(img2)
        shutil.copyfile(img2, op_img2_path)

        self.img1_path = self.getOperImg(op_img1_path)
        self.img2_path = self.getOperImg(op_img2_path)
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

        vbox = QVBoxLayout()
        # 相似度
        ssim_label = QLabel("相似度：98%")
        ssim_label.resize(300, 30)
        ssim_label.setAlignment(Qt.AlignCenter)
        ssim_label.setStyleSheet("color:rgb(10,10,10,255);font-size:18px;font-weight:bold;font-family:Roman times;")
        vbox.addLayout(compare_hbox)
        vbox.addWidget(ssim_label)

        self.setLayout(vbox)

    def connSlot(self):
        # self.btnAdd.clicked.connect(self.btnAddOnClick)
        pass

    def getImgHBox(self, imgLabel, note):
        img_box = QVBoxLayout()
        img_box.addWidget(imgLabel)
        img_box.addLayout(note)
        return img_box

    def getOperImg(self, img, pre=''):
        out_path = './runtime/%s_%s' % (pre, os.path.basename(img))
        gait_view.GR_DrawCalResult(img, out_path)
        return out_path
