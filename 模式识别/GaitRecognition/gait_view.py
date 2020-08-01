import os, shutil
import cv2 as cv

class ImageMng:
    def __init__(self, image_path):
        # 读取原图
        self.src_image = cv.imread(image_path)
        self.opt_image = cv.imread(image_path)

    # 保存图像
    def ImageSave(self, img, file = 'default.jpg'):
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
        print("threshold value %s" % ret)  # 阈值
        self.opt_image = binary
        return binary

    # 找到每行的第一个白点
    def GetFirstWhitePoint(self):
        list_first_white = []
        row, col = self.opt_image.shape
        for i in range(row):
            for j in range(col):
                if self.opt_image[i, j] == 255:
                    list_first_white.append((j, i))
                    break
        return list_first_white

    # 图片中画折线
    def DrawLineSrc(self, list_point):
        for i in range(1, len(list_point)):
            # 起点和终点的坐标
            ptStart = list_point[i - 1]
            ptEnd = list_point[i]
            point_color = (0, 0, 255)  # BGR
            thickness = 1 # 线条宽度
            lineType = 4
            cv.line(self.src_image, ptStart, ptEnd, point_color, thickness, lineType)


def SystemWait():
    cv.waitKey(0)
    cv.destroyAllWindows()
    return True

def GR_DrawBackLine(src_img_path, dst_img_path):
    # 读取原图
    img = ImageMng(src_img_path)
    # img.ImageShow('src')

    # 二值化处理
    img.Binarization()
    # img.ImageShow('bry')

    # 画背部曲线
    list_first_white = img.GetFirstWhitePoint()
    img.DrawLineSrc(list_first_white)
    img.ImageShowSrc('', dst_img_path) # 保存到文件夹，不显示

def main():
    # GR_DrawBackLine('./057.png', './057_out.png')
    # GR_DrawBackLine('./fn00/058.png', './058_out.png')
    # return SystemWait()

    # 绘制整个文件夹
    list_file = os.listdir('./fn00')
    for file in list_file:
        GR_DrawBackLine('./fn00/%s' % file, './output/%s' % file)

    return SystemWait()

if __name__ == '__main__':
    main()