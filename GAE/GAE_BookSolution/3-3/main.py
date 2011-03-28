import cgi

query = cgi.FieldStorage()
name = query.getvalue('who', 'anonymous')

print """Content-Type: text/html

<h1>Hello, %s</h1>""" % name
