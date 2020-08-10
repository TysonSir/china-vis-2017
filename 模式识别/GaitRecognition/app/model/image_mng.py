import cv2 as cv
import os

class ImageMng:
    def __init__(self, image_path):
        # 读取原图
        self.src_image = cv.imread(image_path)
        self.opt_image = cv.imread(image_path)

    # 保存图像
    def ImageSave(self, img, file = 'default.jpg'):
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        cv.imwrite(file, img)

    # 显示图像
    def ImageShow(self, title, savepath=''):
        if title != '':
            cv.namedWindow(title, cv.WINDOW_NORMAL)  # 设置为WINDOW_NORMAL可以任意缩放
            cv.imshow(title, self.opt_image)
        if savepath != '':
            self.ImageSave(self.opt_image, savepath)

    # 显示原图
    def ImageShowSrc(self, title, savepath=''):
        if title != '':
            cv.namedWindow(title, cv.WINDOW_NORMAL) #设置为WINDOW_NORMAL可以任意缩放
            cv.imshow(title, self.src_image)
        if savepath != '':
            self.ImageSave(self.src_image, savepath)

    # 图像二值化处理
    def Binarization(self):
        gray = cv.cvtColor(self.opt_image, cv.COLOR_RGB2GRAY)  # 把输入图像灰度化
        # 直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
        # print("threshold value %s" % ret)  # 阈值
        self.opt_image = binary
        return binary

    # 原图片中画点
    def DrawCenterPointSrc(self, point=(0, 0)):
        point_size = 1
        point_color = (255, 0, 0)  # BGR
        thickness = 4  # 可以为 0 、4、8
        cv.circle(self.src_image, point, point_size, point_color, thickness)

    # 原图片中画折线
    def DrawLineSrc(self, list_point, color=(0, 0, 255)):
        for i in range(1, len(list_point)):
            # 起点和终点的坐标
            ptStart = list_point[i - 1]
            ptEnd = list_point[i]
            point_color = color # BGR
            thickness = 1 # 线条宽度
            lineType = 4
            cv.line(self.src_image, ptStart, ptEnd, point_color, thickness, lineType)