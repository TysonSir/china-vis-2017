import numpy as np 
from matplotlib import pyplot as plt 
from pylab import * 
import pandas as pd
import os

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

data_dir = r'.\data2'

# 返回file_dir文件夹中所有文件路径列表
def file_paths(file_dir):
    list_files = []
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file)
        if not os.path.isdir(file_path):
            list_files.append(file_path)  # 当前路径下所有非目录子文件
    return list_files

print(file_paths(data_dir))

# 从文件中的读取数据存到 all_people 中
all_people = []
for data_file in file_paths(data_dir):
    csv_data = pd.read_csv(data_file)  # 读取训练数据
    all_people += csv_data.values.tolist()

# PERSONID,SITEID,XB,CUSTOMERNAME,ONLINETIME,OFFLINETIME,AREAID,BIRTHDAY
# all_people = [
# ("4911d1b9aa77f09fb6","50010710000149","男","王**","20161008115633","20161008172708","511622","19950529"),
# ("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","431521","19850504"),
# ("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","521622","19950523"),
# ("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","431521","19850504"),
# ("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","521622","19950523"),
# ("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","431521","19850504"),
# ("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","521622","19950523"),
# ("d0a4524541ab02a40e","50010810000102","男","李**","20161008220336","20161009012022","610921","19950217")
# ]

class People:

    PERSONID = '' # 上网人编号
    SITEID = ''
    XB = ''
    CUSTOMERNAME = ''
    ONLINETIME = ''
    OFFLINETIME = ''
    AREAID = ''
    BIRTHDAY = ''

    def __init__(self, src_info):
        self.PERSONID = str(src_info[0]) # 上网人编号
        self.SITEID = str(src_info[1]) # 
        self.XB = str(src_info[2]) # 
        self.CUSTOMERNAME = str(src_info[3]) # 
        self.ONLINETIME = str(src_info[4]) # 
        self.OFFLINETIME = str(src_info[5]) # 
        self.AREAID = str(src_info[6]) # 
        self.BIRTHDAY = str(src_info[7]) # 

dict_group = {}
# 人口按地区分类，数据存入 dict_group 中
for i in all_people:
    peo = People(i)
    # peo.AREAID 的前两个是分类
    peo1 = peo.AREAID[0:2]
    # dict_group['00'] = [People1,People2,People2]
    if peo1 not in dict_group.keys():
        dict_group[peo1] = []
    dict_group[peo1] += [i]

# 画图
x =  dict_group.keys()
y = []
for j in dict_group.values():
    y.append(len(j))

plt.bar(x, y, align =  'center') 
plt.title('各省流动人口数量') 
plt.ylabel('在重庆人口数量')
plt.xlabel('省份编号')
# plt.xticks(x, ('四川','云南','贵州','陕西')) 
plt.show()
# 51四川，53云南，52贵州，61陕西
