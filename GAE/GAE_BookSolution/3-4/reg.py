# -*- coding: utf-8 -*-
import cgi

form = cgi.FieldStorage()
name = form.getvalue('name', '')
email = form.getvalue('email', '')

print """Content-Type: text/html; charset=utf-8

<h1>您註冊的資料如下：</h1>
<ul>
  <li>您的大名: %s</li>
  <li>您的Email: %s</li>
</ul>
""" % (name, email)
