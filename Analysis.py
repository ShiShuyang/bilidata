# -*- coding: gbk -*-
import ssytool

'''
av:
0 av
1 标题
2 mid（UPid）
3 cid
4 时间
5 点击
6 收藏
7 硬币
8 弹幕
9 pid未知
10 类型id

user：
0 昵称
1 mid
2 注册时间戳
3 粉丝数量
4 关注数量
5 等级积分
6 被多少人充电
7 关注列表
'''

def makeFilterList():
    c = ssytool.readCellLines('Accounting/result.txt')
    wholeLength = int(c[-1][0])
    exsist = zip(*c)[0]
    exsist = map(int, exsist)
    notExsist = filter(lambda x: x not in exsist, range(1, wholeLength))
    ssytool.writeText('FilterList.txt', ','.join(map(str, notExsist)))


def singleAvRank():
    l = ssytool.readCellLines('Accounting/result.txt', ',')
    for i, j in zip(range(4, 8), ('时间', '点击', '收藏', '硬币', '弹幕')):
        l.sort(key = lambda x:x[i])
        print j
        for item in l[:20]:
            print item
    
def singleUPRank():
    l = ssytool.readCellLines('Userinfo/result.txt', ',')
    for i, j in zip((3, 5, 6), ('粉丝', '等级积分', '充电')):
        l.sort(key = lambda x:x[i])
        print j
        for item in l[:20]:
            print item    
    
