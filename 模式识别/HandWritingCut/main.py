import os, pprint
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


# 保存图像
def ImageSave(image, file = 'default.jpg'):
    cv.imwrite(file, image)

# 显示图像
def ImageShow(image, title = 'default title', savepath=''):
    cv.namedWindow(title, cv.WINDOW_NORMAL) #设置为WINDOW_NORMAL可以任意缩放
    cv.imshow(title, image)
    if savepath != '':
        ImageSave(image, savepath)

# 图像二值化处理
def Binarization(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  # 把输入图像灰度化
    #直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
    print("threshold value %s" % ret) # 阈值
    return binary

# 将每个列中的黑色像素数相加
def ColBlackPoint(img):
    list=[]
    row, col = img.shape
    for i in range(col):
        list.append((img[:, i] < 200).sum())
    return list

# 将每个行中的黑色像素数相加
def RowBlackPoint(img):
    list=[]
    row, col = img.shape
    for i in range(row):
        list.append((img[i, :] < 200).sum())
    return list

# 图片加框
def AddRectangle(img, x, y, w, h, rgb=(0, 0, 0), pix=2):
    cv.rectangle(img, (x, y), (x + w, y + h), rgb, pix)

# 图片裁剪
def CutRectangle(img, x, y, w, h):
    return img[y:y+h, x:x+w]

# 滑动窗口算法，求低谷区域
def GetLowPointArea(list_data, max_avg=5, min_area = 4):
    left = 0
    right = left + min_area
    list_low_area = []
    start_low = False
    while right < len(list_data):
        list_sub = list_data[left:right]
        avg = sum(list_sub) / len(list_sub)
        if avg > max_avg and not start_low:
            left += 1
            right += 1
        elif avg <= max_avg:
            start_low = True
            right += 1
        elif avg > max_avg and start_low:
            list_low_area.append((left, right))
            left = right
            right = left + min_area
            start_low = False

    return list_low_area

# 获得汉字所在区域
def GetCharArea(list_low_area, img_width, char_min_width=10):
    list_char_area = []
    left = 0
    list_low_area.append((img_width, img_width))
    for l, r in list_low_area:
        char_range = (left, l)
        left = r
        if char_range[1] - char_range[0] > char_min_width:
            list_char_area.append(char_range)
    return list_char_area

def SystemWait():
    cv.waitKey(0)
    cv.destroyAllWindows()
    return True

def init():
    # 创建文件夹
    col_dir = './output/col'
    if not os.path.exists(col_dir):
        os.makedirs(col_dir)

    char_dir = './output/char'
    if not os.path.exists(char_dir):
        os.makedirs(char_dir)
    return col_dir, char_dir

def ColCut(image, col_dir):
    row_num, col_num = image.shape
    # 纵向切分之 求切分范围
    list_col_num = ColBlackPoint(image) # 求所有纵向的 黑色像素点数量
    list_low_area = GetLowPointArea(list_col_num) # 求低谷范围
    list_char_area = GetCharArea(list_low_area, len(list_col_num)) # 求汉字范围

    # 纵向切分之 保存图片
    for x1, x2 in list_char_area:
        cut_bry = CutRectangle(image, x=x1, y=0, w=x2-x1, h=row_num)
        ImageShow(cut_bry, str(x1), savepath=os.path.join(col_dir, '%d_%d.jpg' % (x1, x2)))

def RowCut(image, char_dir):
    bry = Binarization(image)
    row_num, col_num = bry.shape
    # 横向切分之 求切分范围
    list_row_num = RowBlackPoint(bry)  # 求所有横向的 黑色像素点数量
    list_low_area = GetLowPointArea(list_row_num)  # 求低谷范围
    list_char_area = GetCharArea(list_low_area, len(list_row_num))  # 求汉字范围

    # 横向切分之 保存图片
    for y1, y2 in list_char_area:
        cut_bry = CutRectangle(bry, x=0, y=y1, w=col_num, h=y2 - y1)
        ImageShow(cut_bry, str(y1), savepath=os.path.join(char_dir, '0_145_%d_%d.jpg' % (y1, y2)))

def main():
    # 初始化
    col_dir, char_dir = init()

    # 读取原图
    src = cv.imread('./00000142.jpg')
    ImageShow(src, 'src')

    # 二值化处理
    bry = Binarization(src)
    row_num, col_num = bry.shape

    # # 切分区域，保存图片
    # cut_bry = CutRectangle(bry, x=10, y=10, w=100, h=100)
    # ImageShow(cut_bry, 'cut_bry', savepath='cut_bry.jpg')
    #
    # # 图片上画框
    # AddRectangle(bry, x=10, y=10, w=100, h=100)
    # ImageShow(bry, 'Binarization')

    # 纵向切分
    ColCut(bry, col_dir)
    # 横向切分
    image = cv.imread("./output/col/0_145.jpg")
    RowCut(image, char_dir)
    return SystemWait()

    plt.bar(range(len(list_col_num)), list_col_num)

    list_row_num = RowBlackPoint(bry)
    plt.bar(range(len(list_row_num)), list_row_num)
    plt.show()

if __name__ == '__main__':
    main()