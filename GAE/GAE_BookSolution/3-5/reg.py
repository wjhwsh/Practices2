import cgi
import os
from google.appengine.ext.webapp import template

form = cgi.FieldStorage()
name = form.getvalue('name', '')
email = form.getvalue('email', '')

template_path = os.path.join(os.path.dirname(__file__), 'result.html')

print 'Content-Type: text/html;charset=utf-8'
print ''
print template.render(template_path, {'name': name, 'email': email})
