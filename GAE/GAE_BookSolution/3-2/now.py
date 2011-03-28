from datetime import datetime

print """Content-Type: text/html

It is <img src="/s/time.png"><b>%s</b> now.""" % datetime.now()
