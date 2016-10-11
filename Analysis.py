# -*- coding: gbk -*-
import ssytool

'''
av:
0 av
1 ����
2 mid��UPid��
3 cid
4 ʱ��
5 ���
6 �ղ�
7 Ӳ��
8 ��Ļ
9 pidδ֪
10 ����id

user��
0 �ǳ�
1 mid
2 ע��ʱ���
3 ��˿����
4 ��ע����
5 �ȼ�����
6 �������˳��
7 ��ע�б�
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
    for i, j in zip(range(4, 8), ('ʱ��', '���', '�ղ�', 'Ӳ��', '��Ļ')):
        l.sort(key = lambda x:x[i])
        print j
        for item in l[:20]:
            print item
    
def singleUPRank():
    l = ssytool.readCellLines('Userinfo/result.txt', ',')
    for i, j in zip((3, 5, 6), ('��˿', '�ȼ�����', '���')):
        l.sort(key = lambda x:x[i])
        print j
        for item in l[:20]:
            print item    
    
