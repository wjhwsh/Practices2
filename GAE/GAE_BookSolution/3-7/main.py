# -*- coding: utf-8 -*-
import os

def main():
    cookie = os.environ.get('HTTP_COOKIE')
    counter = 0
    if cookie: # 如果有 cookie，看看裡面是不是已經有 counter 值
        pos = cookie.find('counter')
        if pos != -1:
            counter_param = cookie[pos:].split(';')[0]
            counter = int(counter_param.split('=')[1])

    counter = counter + 1
    # 送出新的 counter 值到用戶端的 cookie
    print """Set-Cookie: counter=%d
Content-Type: text/html; charset=utf-8

您已經瀏覽了 <b>%d</b> 次""" % (counter, counter)

if __name__ == '__main__':
    main()
