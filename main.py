#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        div {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
# initialize format vars
userkeep = ""
usererror = ""
passerror = ""
matcherror = ""
emailkeep = ""
emailerror = ""
USER_RE = re.compile(r"^[a-szA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        
class Index(webapp2.RequestHandler):
    def get(self):
        main_form = """
        <form action="/submit" method="post">
            <label>
                Username  <input type="text" name="username" value="{}"/> <div>{}</div> <br> 
                Password  <input type="password" name="password1"/> <div>{}</div> <br> 
                Verify Password  <input type="password" name="password2"/> <div>{}</div> <br> 
                E-mail (optional)  <input type="text" name="email" value="{}"/> <div>{}</div> 
            </label>
            <input type="submit" name="submit"/>
        </form>
        """.format(self.request.get("userkeep"), self.request.get("usererror"), self.request.get("passerror"), self.request.get("matcherror"), self.request.get("emailkeep"), self.request.get("emailerror"))
        
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""
        
        self.response.write(page_header + main_form + page_footer)

class Verify(webapp2.RequestHandler):

    def valid_username(self, username):
        return USER_RE.match(username)
        
    def valid_password(self, password):
        return PASS_RE.match(password)
        
    def valid_email(self, email):
        return EMAIL_RE.match(email)

    def post(self):
    	error = ""
        # verification
        if not self.valid_username(self.request.get("username")):
            if error != "":
                error += "&"
            error += "usererror=" + "That is not a valid username."
        if not self.valid_password(self.request.get("password1")):
            if error != "":
                error += "&"
            error += "passerror=" + "That is not a valid password."
        if not self.valid_email(self.request.get("email")) and self.request.get("email") != "":
            if error != "":
                error += "&"
            error += "emailerror=" + "That is not a valid E-mail."
        if self.request.get("password1") != self.request.get("password2"):
            if error != "":
                error += "&"
            error += "matcherror=" + "Those passwords do not match."
        
        # other stuff
        userkeep = self.request.get("username")
        emailkeep = self.request.get("email")
        
        # welcome page
        if error == "":
            response = page_header + "Welcome!" + page_footer
            self.response.write(response)
        else:
            self.redirect("/?" + error + "&userkeep=" + userkeep + "&emailkeep=" + emailkeep)
app = webapp2.WSGIApplication([
    ('/', Index),
    ('/submit', Verify)
], debug=True)
