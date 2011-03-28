#!/usr/bin/python
# -*- coding:gbk -*-
#usage:
#-h,     --help          This message
#-s,     --song_name     Download single song
#-t1,    --top=1         Download Baidu NewSong Top 100
#-t2,    --top=2         Download Baidu Song Top 500


import urllib
import htmllib
import formatter
import string
import os
import sys
import thread
import re
import subprocess
import getopt
#import threading

# 常量定義
# ###############################################################
BaiduTopList=[
# baidu新歌TOP100 鏈接
"http://list.mp3.baidu.com/list/newhits.html",
# baidu歌曲TOP500 鏈接
"http://list.mp3.baidu.com/topso/mp3topsong.html"
]
# 百度歌曲搜索
BaiduSongSearch="http://mp3.baidu.com/m?f=ms&tn=baidump3&ct=134217728&lf=&rn=&word=SONG_NAME&lm=0"

#下載的歌曲的最大數目
MAX_SONGS=100
# 歌曲最小大小

SONG_MINSIZE=2
SONG_MAXSIZE=8
SONG_SIZEUNIT=1024*1024
# 文件覆蓋
OVERWRITE=False

# 全局變量



def DownMp3(url,song_name_prefix):
    SongLink = GetSongLink(url) 
    #print SongLink
    for item in SongLink:
        # index song_name songer mp3 size 
        print "\t"+item[0]+"."+item[2]+"-"+item[4]+"."+item[6]+":"+item[5]+"M" #+item[1]
        if item[6] !="mp3":
            print "\tSkip",item[6]
            continue
        if string.atof(item[5]) <SONG_MINSIZE or string.atof(item[5]) >SONG_MAXSIZE:
            print "\tSkip",item[5],"M"
            continue
        song_name=song_name_prefix+item[2]+"_"+item[4]+".mp3"
        
        url2=UncodeUrl(item[1])
        content = DownObjectByUrl(url2)
        # baidu 解碼 url
        mp3url = BaiduUncodingUrl(content)
        
        retCode=SaveFile(mp3url, ".",song_name)
        if retCode == 0 or retCode == 5:
            break; 


def SaveFile(url, path,filename):
    """ 
    下載url指定的網絡資源對象
    return result
    0 成功
    1 wget error, 2 User interrupt, 3 Execution failed, 4 size error, 5 file exist     
    """
    if not OVERWRITE:
        if os.path.exists(path+"\\"+filename):
            if os.path.getsize(path+"\\"+filename) > SONG_MINSIZE*SONG_SIZEUNIT :
                print filename+":exist"
                return 5
    
    url2 = UncodeUrl(url)
    print "\t"+path+"\\"+filename+" : "+url2
    cmd='wget -O'+filename+' -t5 -w2 -T10 '+url2
    #os.system(cmd)
    try:
        retcode = subprocess.call(cmd, shell = True)
        print "wget return code:",retcode
        if retcode!=0 :
            print "\tFailed"
            return 1
    except KeyboardInterrupt,e:
        print >>sys.stderr, "User Interrupt!",e
        return 2
    except OSError,e:
        print >>sys.stderr, "Execution failed!",e
        return 3
    
    if os.path.getsize(path+"\\"+filename) <SONG_MINSIZE*SONG_SIZEUNIT :
        print "\tFailed!"
        return 4
    print "\tOK"
    return 0



def UncodeUrl(url):
    """ url decode，主要是處理中文進行unicode編碼的問題 """
    url2 = ""
    b = 0
    for c in url:
            i = ord(c)
            if b == 1:
                    b = 0
                    url2 += "%"
                    s = repr(hex(i))
                    url2 += s[-3] + s[-2]
                    continue
            if i >= 0x80:
                    url2 += "%"
                    s = repr(hex(i))
                    url2 += s[-3] + s[-2]
                    b = 1
            elif c == ' ':
                    url2 += "%20"
            else:
                    url2 += c
    return url2

def GetBaiduNextPageUrl(url):
        global pn
        url += "&rn=" + repr(rn) + "&pn=" + repr(pn) + "&ln=" + repr(ln)
        pn += 18
        return url

def DownObjectByUrl(url):
    try:
        fp = urllib.urlopen(url)
        content = ""
        sys.stdout.write("|")
        while 1:
            s = fp.read(8192)
            if not s:
                    break
            content += s
            sys.stdout.write("-")
            #print "=", 
        fp.close()
        print "|"
        return content
            
    except :
        print "\tConnect error! "
        return ""
        
def GetTopLists(url):
    html = DownObjectByUrl(url)
    rePattern = """<td width="3%"[^>]+>([\d]+)\.</td>\s+<td width="17%"[^>]+><a href="([^"]+)" target=_blank>[<b>]*([^<]*)[</b>]*</a>"""
    reTop = re.compile(rePattern,re.S)
    return reTop.findall(html)
def GetSongLink(url):
    """ 
    0:index, 1:link, 2:song name 3:none 4:singer 5:size 6:type
    """
    html = DownObjectByUrl(url)
    rePattern = """<tr>\s+<td class=tdn>(\d+)</td>\s+<td class=d><a href="([^"]+)" title=[^#]+[^>]+>([^<]+)</font>[^\n]+\s+<td><a href[^>]+>(<font color="#c60a00">)?([^<]+)<[^\n]+\s+[^\n]+\s+[^\n]+\s+[^\n]+\s+[^\n]+\s+<td>(\d+.\d+)\s+M</td>\s+<td>([^<]+)</td>"""
    reTop = re.compile(rePattern,re.S)
    return reTop.findall(html) 


#-------- 破解baidu對url的變形處理，從加密的url還原出正確的mp3鏈接 --------------

def N(K,H,S,P,Q):
    #K存儲ASCII字符 H存儲字符在K中的位置，如Z(ASCII:90) H(90)=Z在K中的位置
    for R in range(S, P+1):
        K[R]=R+Q
        #print "K R=",R,K[R]
        H[R+Q]=R 
    return (K,H)

def A(K,H,M,Q):
        #如Q="w884://0p2C9t6t2.CqEw.2t8/q03v/j403psUx0t7/HFFN-O/ONLJMKNH.14I"
        #print "Q=",Q
        #print "M=",M
        
        #for R in range(0,61):
        # print "K",R,K[R]
        P=len(Q)
        S=""
        for R in range(0, P):
                T=Q[R]
                #字符需要做變換
                if T >= 'A' and T <= 'Z' or T >= 'a' and T <= 'z' or T >= '0' and T <= '9':
                        
                        i = ord(T) #T的ASCII碼
                        U = H[i] - M #在K中的映射-M偏移
                        if U < 0:
                                U+=62
                        
                        T = chr(K[U])
                        
                S+=T
        return S
def GetBaiduFLJ(content):
    """ 獲取進行baidu mp3路徑解密的F/L/J """

    k = content.find("var F=")
    if k == -1:
            return 0
    k += len("var F=")
    str = content[k:-1]
    k = str.find(",")
    if k == -1:
            return 0
    F = str[:k]
    k = str.find("var I=")
    if k == -1:
            return 0
    k += len("var I=") + 1
    str2 = str[k:-1]
    k = str2.find("\"")
    if k == -1:
            return 0
    L = str2[:k]

    k = str2.find("J=")
    if k == -1:
            return 0
    k += len("J=") + 1
    str3 = str2[k:-1]
    k = str3.find("\"")
    if k == -1:
            return 0
    J = str3[:k]
    #print "F=", F
    #print "L=", L
    #print "J=", J 
    return [F,L,J]






def BaiduUncodingUrl(content):
    #baidu mp3 url 鏈接變形元素

    M = 0
    K=[]
    H=[]

    for i in range(0, 127):
            K.append(0)

    for j in range(0, 127):
            H.append(0)    

    [F,L,J]=GetBaiduFLJ(content)

    O=""
    E=""
    
    K,H=N(K,H,0,9,48) #K(0-9)='0'-'9' 
    K,H=N(K,H,10,35,55) #K(10-35)='A'-'Z'
    K,H=N(K,H,36,61,61) #K(36-61)='a'-'z'
    #K:
    #0 1 2 3 4 5 6
    #012345678901234567890123456789012345678901234567890123456789012
    #01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    
    M=string.atol(F)%26 #取餘數，26個英文字符，M為偏移量
    if not M:
            M = 1
    
    O=A(K,H,M,L)
    if L == J:
            E = O
    else:
            E = A(K,H,M,J)
    #print "A(L)=O:",O
    #print "A(J):",A(J)
    return E 


def DownloadTopListSong(TopList):
    #獲取歌曲鏈接 
    listSonglinks = GetTopLists(TopList)
    count=0
    for item in listSonglinks:
        # index song name
        print item[0]+"."+item[2] #+":"+item[1]
    #lm= '-1'=任意 '0'=mp3 '1'=rm '2'=wma '3'=asf '4'=ram '5'=mid '6'=flash 
        rePattern = "lm=-1&"
        reTop = re.compile(rePattern,re.S)
        urlMp3List=reTop.sub("lm=0&",item[1])
        song_name=string.zfill(item[0],3)+"."
        DownMp3(urlMp3List,song_name)
        count=count+1
        if count>=MAX_SONGS:
            break
            
def DownloadSingleSong(song_name):
    print song_name
    rePattern = "SONG_NAME"
    reTop = re.compile(rePattern,re.S)
    urlMp3List=reTop.sub(song_name,BaiduSongSearch)
    
    url2=UncodeUrl(urlMp3List)
    print url2
    DownMp3(url2,"")
    
def usage():
    print "Usage: "
    print "-h,    --help        This message"
    print "-s,    --song_name    Download single song"
    print "-t1,    --top=1        Download Baidu NewSong Top 100"
    print "-t2,    --top=2        Download Baidu Song Top 500"
    


def main():
    if len(sys.argv) < 2 :
        usage()
        sys.exit()
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "hs:t:", ["help", "song_name=","top="])
    except getopt.GetoptError,err:
        print "Error:",str(err),"\n"
        usage()
        sys.exit(2) 
    for o,v in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit()
        elif o in ("-s","--song_name"):
            song_name = v
            DownloadSingleSong(song_name)
        elif o in ("-t","--top"):
            print "-t",v
            DownloadTopListSong(BaiduTopList[string.atoi(v)-1])
        else:
            print "Unknown parameter!"
            sys.exit()

if __name__ == "__main__":
    main()
