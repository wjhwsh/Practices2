# load a given picture from a web page and save it to a file
# (you have to be on the internet to do this)
# tested with Python24     vegaseat     19sep2006

import urllib2
import webbrowser
import os

# find yourself a picture on a web page you like
# (right click on the picture, look under properties and copy the address)
picture_page = "http://www.google.com/intl/en/images/logo.gif"

#webbrowser.open(picture_page)  # test

# open the web page picture and read it into a variable
opener1 = urllib2.build_opener()
page1 = opener1.open(picture_page)
my_picture = page1.read()

# open file for binary write and save picture
# picture_page[-4:] extracts extension eg. .gif
# (most image file extensions have three letters, otherwise modify)
filename = "my_image" + picture_page[-4:]
print filename  # test
fout = open(filename, "wb")
fout.write(my_picture)
fout.close()

# was it saved correctly?
# test it out ...
webbrowser.open(filename)

# or ...
# on Windows this will display the image in the default viewer
#os.startfile(filename)
