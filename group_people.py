# 读取数据存入列表
# C:\Users\HJY\Desktop\可视化项目\hydata_swjl_3.csv
import pandas as pd
import os

def file_paths(file_dir):
    list_files = []
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file)
        if not os.path.isdir(file_path):
            list_files.append(file_path)  # 当前路径下所有非目录子文件
    return list_files

# print(file_names('../'))

all_people = []
for data_file in file_paths('../'):
    csv_data = pd.read_csv(data_file)  # 读取训练数据
    all_people += csv_data.values.tolist()

# print(csv_data.shape)  # (189, 9)
# print(csv_data)  # (189, 9)
# print(type(csv_data[0:3]))
# print(list_data)

# # PERSONID,SITEID,XB,CUSTOMERNAME,ONLINETIME,OFFLINETIME,AREAID,BIRTHDAY
# all_people = [
# ("4911d1b9aa77f09fb6","50010710000149","男","王**","20161008115633","20161008172708","511622","19950529"),
# ("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","531521","19850504"),
# ("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","561622","19950523"),
# ("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","531521","19850504"),
# ("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","561622","19950523"),
# ("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","531521","19850504"),
# ("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","561622","19950523"),
# ("d0a4524541ab02a40e","50010810000102","男","李**","20161008220336","20161009012022","600921","19950217")
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
        self.PERSONID = src_info[0] # 上网人编号
        self.SITEID = src_info[1] # 
        self.XB = src_info[2] # 
        self.CUSTOMERNAME = src_info[3] # 
        self.ONLINETIME = src_info[4] # 
        self.OFFLINETIME = src_info[5] # 
        self.AREAID = src_info[6] # 
        self.BIRTHDAY = src_info[7] # 

dict_group = {}

# peo = People( (1,2) )
# peo.AREAID 的前两个是分类

# dict_group['00'] = [People1,People2,People2]
# dict_group['01'] = [People3,People4]

# 人口按地区分类，数据存入 dict_group 中




# 输出
