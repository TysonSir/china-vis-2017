import os

from model import gait_view

class CompareResult:
    area_diff = 0
    height_diff = 0

    def calPercent(self):
        return 100 - self.area_diff//10 - self.height_diff


class MatchAlgo:
    area_diff = 220
    height_diff = 10

    def isImageSame(self, img1, img2, result=CompareResult()):
        list_back1 = self.getLeftLine(img1)
        list_back2 = self.getLeftLine(img2)

        same_val = 0 # 相似个数

        # 身高比较
        img1_h = self.getWidth(list_back1, 1) # 纵向宽度
        img2_h = self.getWidth(list_back2, 1) # 纵向宽度

        result.height_diff = abs(img1_h - img2_h)
        if result.height_diff > self.height_diff: # 身高差大于height_diff像素
            return False
        same_val += 1

        # 曲线像素差
        distance = self.getMin(list_back1, 0)
        self.leftMv(list_back1, distance)
        distance = self.getMin(list_back1, 1)
        self.topMv(list_back1, distance)

        distance = self.getMin(list_back2, 0)
        self.leftMv(list_back2, distance)
        distance = self.getMin(list_back2, 1)
        self.topMv(list_back2, distance)

        result.area_diff = self.crossArea(list_back1, list_back2)
        if result.area_diff > self.area_diff: # 像素差大于area_diff
            return False
        same_val += 1

        return True

    def getLeftLine(self, img_path):
        # 读取原图
        img = gait_view.GaitImage(img_path)
        # img.ImageShow('src')

        # 二值化处理
        img.Binarization()
        # img.ImageShow('bry')

        # 获得背部曲线
        list_point = img.GetFirstWhitePointOnline()
        list_rslt = [[point[0], point[1]] for point in list_point]
        return list_rslt

    def getWidth(self, list_points, idx=0):
        min_x = 9999
        max_x = 0
        for point in list_points:
            x = point[idx]
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
        return max_x - min_x

    def getMin(self, list_points, idx=0):
        min_x = 9999
        for point in list_points:
            x = point[idx]
            if x < min_x:
                min_x = x
        return min_x

    def leftMv(self, list_points, distance=0):
        for point in list_points:
            point[0] -= distance
        return list_points

    def topMv(self, list_points, distance=0):
        for point in list_points:
            point[1] -= distance
        return list_points

    def crossArea(self, list_point1, list_point2):
        area = 0
        limit = min(len(list_point1), len(list_point2))
        for i in range(limit):
            x1 = list_point1[i][0]
            x2 = list_point2[i][0]
            area += abs(x1 - x2)
        return area