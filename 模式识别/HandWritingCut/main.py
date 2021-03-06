import os, shutil
import cv2 as cv
from pylab import *
from matplotlib import pyplot as plt
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

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
def AddRectangle(img, x, y, w, h, rgb=(0, 0, 255), pix=3):
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
    # 删除旧文件夹
    output_dir = './output'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
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
    plt.bar(range(len(list_col_num)), list_col_num)
    plt.title('像素点横坐标与该列黑像素点个数关系图')
    plt.ylabel('黑像素点个数')
    plt.xlabel('像素点横坐标')
    plt.show()
    list_low_area = GetLowPointArea(list_col_num) # 求低谷范围
    list_char_area = GetCharArea(list_low_area, len(list_col_num)) # 求汉字范围

    # 纵向切分之 保存图片
    for x1, x2 in list_char_area:
        cut_bry = CutRectangle(image, x=x1, y=0, w=x2-x1, h=row_num)
        ImageSave(cut_bry, os.path.join(col_dir, '%d_%d.jpg' % (x1, x2)))

def RowCut(image, char_dir, prefix):
    bry = Binarization(image)
    row_num, col_num = bry.shape
    # 横向切分之 求切分范围
    list_row_num = RowBlackPoint(bry)  # 求所有横向的 黑色像素点数量
    list_low_area = GetLowPointArea(list_row_num)  # 求低谷范围
    list_char_area = GetCharArea(list_low_area, len(list_row_num))  # 求汉字范围

    # 横向切分之 保存图片
    for y1, y2 in list_char_area:
        cut_bry = CutRectangle(bry, x=0, y=y1, w=col_num, h=y2 - y1)
        ImageSave(cut_bry, os.path.join(char_dir, '%s_%d_%d.jpg' % (prefix, y1, y2)))

def main():
    # 初始化
    col_dir, char_dir = init()

    # 读取原图
    src = cv.imread('./00000142.jpg')
    ImageShow(src, 'src')

    # 降噪
    noise = cv.GaussianBlur(src, (7, 7), 0)
    ImageShow(noise, 'GaussianBlur', './output/noise.jpg')

    # 二值化处理
    bry = Binarization(noise)
    ImageShow(bry, 'bry','./output/bry.jpg')

    # 纵向切分
    ColCut(bry, col_dir)
    # 横向切分
    for filename in os.listdir(col_dir):
        image = cv.imread(os.path.join(col_dir, filename))
        RowCut(image, char_dir, prefix=filename.split('.')[0])

    # 原图中框出汉字
    for filename in os.listdir(char_dir):
        list_num = filename.split('.')[0].split('_')
        x1 = int(list_num[0])
        x2 = int(list_num[1])
        y1 = int(list_num[2])
        y2 = int(list_num[3])
        # 图片上画框
        AddRectangle(src, x=x1, y=y1, w=x2 - x1, h=y2 - y1)
    ImageShow(src, 'src', savepath='./output/out.jpg')


    return SystemWait()

if __name__ == '__main__':
    main()