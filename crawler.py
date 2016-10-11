# -*- coding: utf8 -*-
import urllib2, multiprocessing, zlib, re, time
from StringIO import StringIO
import gzip, json, random


#f = open('cookie', 'r')
mycookie =  ''
#f.close()

def reMatch(start, end, s):
    #正则表达用来找需要的数据
    query = start + '.+?' + end
    q = re.findall(query, s)
    if q:
        return q[0][len(start): -len(end)]
    else:
        return

def openurl(url, postdata = '', referer = ''):
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    request.add_header('Cookie', mycookie)
    if referer:
        request.add_header('Referer', referer)
    opener = urllib2.build_opener()
    try:
        if postdata:
            f = opener.open(request, data=postdata, timeout = 10)
        else:
            f = opener.open(request, timeout = 10)
        isGzip = f.headers.get('Content-Encoding')
        if isGzip :
            compresseddata = f.read()
            compressedstream = StringIO(compresseddata)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
        else:
            data = f.read()
        return data
    except Exception, e:
        if ('timed out' in str(e)) or ('10054' in str(e)) or ('400' in str(e)) or ('504' in str(e)):
            print 'Urlopen retry', e, url, postdata
            time.sleep(random.random()*10)
            return openurl(url, postdata, referer)
        else:
            print 'Urlopen error', e, url
            return

def XMLinfo(cid, av=0):
    # 获取一个视频的具体信息，包括点击、硬币、弹幕数、收藏数、是否只有会员知道的世界等。
    url = 'http://interface.bilibili.com/player?id=cid:{0}&aid={1}'.format(str(cid), str(av)) #这句话现在没有用了但是我还是先留着吧
    url = 'http://interface.bilibili.com/player?id=cid:' + str(cid)
    content = openurl(url)
    xmlitem = ['click',  'favourites', 'coins', 'danmu', 'pid', 'typeid']
    return [reMatch('<{0}>'.format(i), '</{0}>'.format(i), content) for i in xmlitem]

def HTMLinfo(av):
    #获取当前av号对应的HTML页面的信息、包括UP主、标题、上传时间、cid等。如果和谐则返回None。
    url = 'http://www.bilibili.com/video/av' + str(av)
    content = openurl(url)
    if content:
        title = reMatch('<h1 title=\"', '\">', content)
        card = reMatch('card=\"', '\" mid', content)
        mid = reMatch('mid=\"', '\" title', content)
        cid = reMatch('\"cid=', '&aid', content)
        startData = reMatch('<i>', '</i>', content)
        if cid:
            return [av, title, mid, cid, startData]
    return 


def mainThread(threadID = 0, START = 0, END = 1000):
    #获取视频信息的主线程
    f = open('Accounting/' + str(threadID) + '.data', 'w')
    for av in xrange(START, END):
        if not av % 200:
            print time.ctime(), threadID, av - START
        fullInfo = HTMLinfo(av)
        if fullInfo:
            detail = XMLinfo(fullInfo[3])
            fullInfo += detail
            sentence = ','.join(map(lambda x: str(x).replace(',', '，'), fullInfo))
            #print sentence
            #对应 AV、标题、Mid、cid、上传日期、点击、收藏、硬币、弹幕、一个未知id、类别id
            f.write(sentence + '\n')
    f.close()
    print 'Thread', threadID, 'finished.'
        
def reduceFile(path, threadNum):
    #把多线程计算得到的文件合并成一个。
    f = open('path' + '/' + 'result.csv', 'w')
    for i in xrange(threadNum):
        fr = open('path' + '/' + str(i), 'r')
        c = fr.read()
        fr.close()
        f.write(c)
    f.close()

def Userinfo(threadID = 0, START = 0, END = 1000):
    #获取用户的详细信息，具体内容见最后一行注释。
    f = open('Userinfo/' + str(threadID) + '.data', 'w')
    for mid in xrange(START, END):
        if not mid % 200:
            print time.ctime(), threadID, mid - START
        s, mid = '', str(mid)
        #获取mid用户被充电人数
        c = openurl('http://elec.bilibili.com/api/query.rank.do?mid=' + mid)
        try:
            c = json.loads(c)
        except:
            print c
        if c['code'] == 0:
            elec = c['data']['total_count']
        else:
            elec = 0

        #获取基本信息
        c = openurl('http://space.bilibili.com/ajax/member/GetInfo', 'mid=' + mid, 'http://space.bilibili.com/' + mid)
        c = json.loads(c)

        if c['status']:
            query = ['mid', 'regtime', 'fans', 'friend']
            s = c['data']['name'] + ','
            for i in query:
                s += str(c['data'][i]) + ','
            s += str(c['data']['level_info']['current_exp'])+ ','
            s += '|'.join(map(str, c['data']['attentions']))
            # 姓名，mid，注册时间，粉丝数，关注数，积分，关注列表
            f.write(s.encode('utf8') + '\n')
    f.close()
    

if __name__ == '__main__':
    task = 3
    threadNum = 12
    if task == 1:
        Userinfo(0, 3076797, 3076799)
        #mainThread()
    elif task == 2:
        print 'Starting main thread.'
        START, END = 1, 6700000
        for i in xrange(threadNum):
            print str(i), START+(END-START)/threadNum*i, START+(END-START)/threadNum*(i+1)
            multiprocessing.Process(target=mainThread, args=(str(i), START+(END-START)/threadNum*i, START+(END-START)/threadNum*(i+1))).start()
    elif task == 3:
        print 'Starting user thread.'
        START, END = 1, 49228620
        for i in xrange(threadNum):
            print str(i), START+(END-START)/threadNum*i, START+(END-START)/threadNum*(i+1)
            multiprocessing.Process(target=Userinfo, args=(str(i), START+(END-START)/threadNum*i, START+(END-START)/threadNum*(i+1))).start()      
    else:
        reduceFile('Accounting', threadNum)
