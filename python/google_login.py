import urllib
import urllib2
import getpass
import re

email = raw_input("Enter your Google username: ")
password = getpass.getpass("Enter your password: ")

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)

# Define URLs
loing_page_url = 'https://www.google.com/accounts/ServiceLogin'
authenticate_url = 'https://www.google.com/accounts/ServiceLoginAuth'
gv_home_page_url = 'https://www.google.com.tw/dictionary/wordlist?hl=zh-TW'

# Load sign in page
login_page_contents = opener.open(loing_page_url).read()

# Find GALX value
galx_match_obj = re.search(r'name="GALX"\s*value="([^"]+)"', login_page_contents, re.IGNORECASE)

galx_value = galx_match_obj.group(1) if galx_match_obj.group(1) is not None else ''

# Set up login credentials
login_params = urllib.urlencode( {
   'Email' : email,
   'Passwd' : password,
   'continue' : 'https://www.google.com/voice/account/signin',
   'GALX': galx_value
})

# Login
opener.open(authenticate_url, login_params)

# Open GV home page
gv_home_page_contents = opener.open(gv_home_page_url).read()

# Fine _rnr_se value
key = re.search('name="_rnr_se".*?value="(.*?)"', gv_home_page_contents)
print key
print gv_home_page_contents


