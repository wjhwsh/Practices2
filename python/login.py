import sys
import chilkat

req = chilkat.CkHttpRequest()
http = chilkat.CkHttp()

#  Any string unlocks the component for the 1st 30-days.
success = http.UnlockComponent("Anything for 30-day trial")
if (success != True):
    print http.lastErrorText()
    sys.exit()

#  Cookies may be persisted to a directory in the filesystem,
#  or alternatively cached in memory by using the "memory"
#  keyword:
http.put_CookieDir("memory")
#  Accumulated cookies are sent with each GET/POST:
http.put_SaveCookies(True)
#  Cookies received in HTTP responses are to be saved:
http.put_SendCookies(True)

#  Get the page with the login form.  We're only doing this
#  just in case there are cookies that need to be cached
#  and re-sent in the next step:

html = http.quickGetStr("https://secure.del.icio.us/login")
if (http.get_LastStatus() != 200):
    print http.lastErrorText()
    sys.exit()

#  Examining the "Page Info" in FireFox reveals a form with
#  a target of https://secure.del.icio.us/login with
#  fields of "user_name", "password", and "login".  The "login"
#  field is nothing more than the submit button and holds
#  the value "log in".

#  Build an HTTP POST Request:
req.UsePost()
req.put_Path("/login")
req.AddParam("user_name","chilkatsoft")
req.AddParam("password","****")
req.AddParam("login","log in")

#  Send the HTTP POST and get the response.  Note: This is a blocking call.
#  The method does not return until the full HTTP response is received.

domain = "secure.del.icio.us"
port = 443
ssl = True

resp = http.SynchronousRequest(domain,port,ssl,req)
if (resp == None ):
    print http.lastErrorText()
else:
    responseStatus = resp.get_StatusCode()
    if (responseStatus == 302):

        #  We have a redirect.  Follow it...
        #  Note: the FollowRedirects property causes
        #  301/302 responses to GET requests to be
        #  automatically followed.
        http.put_FollowRedirects(True)
        html = http.quickGetStr(resp.getHeaderField("Location"))
        if (http.get_LastStatus() != 200):
            print http.lastErrorText()
            sys.exit()

    else:
        html = resp.bodyStr()

    print str(responseStatus)

    #  Display the HTML source of the page returned.
    print html

