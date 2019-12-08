import numpy as np 
from matplotlib import pyplot as plt 
from pylab import * 
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
# 读取数据存入列表

# PERSONID,SITEID,XB,CUSTOMERNAME,ONLINETIME,OFFLINETIME,AREAID,BIRTHDAY
all_people = [
("4911d1b9aa77f09fb6","50010710000149","男","王**","20161008115633","20161008172708","511622","19950529"),
("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","431521","19850504"),
("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","521622","19950523"),
("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","431521","19850504"),
("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","521622","19950523"),
("016a5cd4d0818fe8cf","50010510000195","男","张**","20161008151632","20161008191536","431521","19850504"),
("837510e352cd784913","50010610002096","男","张**","20161009103815","20161009202937","521622","19950523"),
("d0a4524541ab02a40e","50010810000102","男","李**","20161008220336","20161009012022","610921","19950217")
]

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

# peo = People( (1,2) )
i = 0
while i <= 7:
    peo = People(all_people[i])
    # peo.AREAID 的前两个是分类
    peo1 = peo.AREAID[0:2]
    # dict_group['00'] = [People1,People2,People2]
    if peo1 in dict_group.keys():
        dict_group[peo1] += [all_people[i]]
    else:
        dict_group[peo1] = []
        dict_group[peo1] += [all_people[i]]
    i += 1
# dict_group['01'] = [People3,People4]

# 人口按地区分类，数据存入 dict_group 中

# a = np.array([22,87,5,43,56,73,55,54,11,20,51,5,79,31,27]) 
# plt.hist(a, bins =  [51,53,56,60]) 
# plt.title("histogram") 
# plt.show()
j = 0

x =  dict_group.keys()
y = []
# while j <= len(dict_group.keys()) - 1:

#     y +=  [len(dict_group[j])] 
#     j += 1
for j in dict_group.values():
    y.append(len(j))
plt.bar(x, y, align =  'center') 

plt.title('各省流动人口数量') 
plt.ylabel('Y axis') 
plt.xlabel('X axis')
# plt.xticks(x, ('四川','云南','贵州','陕西')) 
plt.show()
# 51四川，53云南，52贵州，61陕西

# 输出
