import os

def main():
    ua = os.environ.get('HTTP_USER_AGENT')
    print """Content-Type: text/html

Your browser's User-Agent is [ <b>%s</b> ]""" % ua
    
if __name__ == '__main__':
    main()
