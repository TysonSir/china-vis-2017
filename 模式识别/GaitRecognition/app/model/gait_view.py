import os, shutil, math
import cv2 as cv
import matplotlib.pyplot as plt
from model.image_mng import ImageMng

class GaitMath:
    def GetTwoPointDistance(self, point1=(0, 0), point2=(0, 0)):
        x = point1[0] - point2[0]
        y = point1[1] - point2[1]
        #用math.sqrt（）求平方根
        return math.sqrt((x**2)+(y**2))

    def GetDistanceVector(self, point1=(0, 0), list_point=[(0, 0)]):
        list_distance = []
        for point2 in list_point:
            list_distance.append(self.GetTwoPointDistance(point1, point2))
        return list_distance, len(list_distance)

class GaitImage(ImageMng):
    def __init__(self, image_path):
        # 读取原图
        super(GaitImage, self).__init__(image_path)

    # 找到每行的第一个白点
    def GetFirstWhitePointOnline(self):
        list_first_white = []
        row, col = self.opt_image.shape
        for i in range(row):
            for j in range(col):
                if self.opt_image[i, j] == 255:
                    list_first_white.append((j, i))
                    break
        return list_first_white

    # 找质心
    def GetCenter(self):
        x = 0
        y = 0
        row, col = self.opt_image.shape
        # 获取所有白点数量
        cnt_white = 0
        for i in range(row):
            for j in range(col):
                if self.opt_image[i, j] == 255:
                    cnt_white += 1

        target_white = cnt_white // 2

        # 找到竖向中心坐标
        y = 0
        tmp_white = 0
        for i in range(row):
            tmp_white += (self.opt_image[i, :] == 255).sum()
            if tmp_white >= target_white:
                y = i
                break

        # 找到横向中心坐标
        x = 0
        tmp_white = 0
        for j in range(col):
            tmp_white += (self.opt_image[:, j] == 255).sum()
            if tmp_white >= target_white:
                x = j
                break

        return x, y

    # 算步长
    def GetWidthMax(self):
        row, col = self.opt_image.shape
        # 找横向最宽起始点
        max_width = 0 # 最宽长
        max_start = 0  # 最宽起点
        y = 0 # 坐标
        for i in range(row):
            # 该行第一个白色
            start = 0
            for j in range(col):
                if self.opt_image[i, j] == 255:
                    start = j
                    break

            # 该行最后一个白色
            end = 0
            for j in reversed(range(col)):
                if self.opt_image[i, j] == 255:
                    end = j
                    break

            tmp_width = end - start
            if tmp_width > max_width:
                max_start = start
                max_width = tmp_width
                y = i

        return max_start, max_width, y

    # 获取人高度范围
    def GetHightRange(self):
        top = 0
        row, col = self.opt_image.shape
        for i in range(row):
            if top == 0 and (self.opt_image[i, :] == 255).sum() > 0:
                top = i

        bottom = 0
        for i in reversed(range(row)):
            if bottom == 0 and (self.opt_image[i, :] == 255).sum() > 0:
                bottom = i

        return top, bottom


def SystemWait():
    cv.waitKey(0)
    cv.destroyAllWindows()
    return True

def GR_DrawCalResult(src_img_path, dst_img_path):
    gm = GaitMath()

    # 读取原图
    img = GaitImage(src_img_path)
    # img.ImageShow('src')

    # 二值化处理
    img.Binarization()
    # img.ImageShow('bry')

    # 画背部曲线
    list_first_white = img.GetFirstWhitePointOnline()
    img.DrawLineSrc(list_first_white)

    # 画质心
    point_center = img.GetCenter()
    img.DrawCenterPointSrc(point_center)

    # 背部曲线到质心距离向量
    list_distance, count = gm.GetDistanceVector(point_center, list_first_white)
    # plt.scatter(range(count), list_distance)
    # plt.show()

    # 画步长
    max_start, max_width, y = img.GetWidthMax()
    top, bottom = img.GetHightRange()
    img.DrawLineSrc([(max_start, bottom + 5), (max_start + max_width, bottom + 5)], color=(0, 255, 0))

    # 保存到文件夹，不显示
    img.ImageShowSrc('', dst_img_path)

def GR_GetStepLength(img_path):
    # 读取原图
    img = GaitImage(img_path)

    # 二值化处理
    img.Binarization()

    # 获取步长
    max_start, max_width, y = img.GetWidthMax()
    return max_width

def main():
    GR_DrawCalResult('./fn00/057.png', './057_out.png')
    return SystemWait()

    # 绘制整个文件夹
    input_dir = './fn00'
    output_dir = './output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    list_file = os.listdir(input_dir)
    i = 0
    all = len(list_file)
    for file in list_file:
        i += 1
        print('[%d/%d] %s' % (i, all, file))
        GR_DrawCalResult(os.path.join(input_dir, file), os.path.join(output_dir, file))

    return SystemWait()

if __name__ == '__main__':
    main()