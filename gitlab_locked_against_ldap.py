#!/usr/bin/python3
import os
import time
import json
import sys
sys.path.insert(0, '/var/lib/aditianal_files') # path to creds file - volt or clear text
import creds
import requests
import smtplib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from datetime import date
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

today_utc = date.today()
today_human = today_utc.strftime("%d/%m/%Y")


helper_string = ""
gitlab_res = requests.get("https://gitlab.companey.com/api/v4/users?blocked=true&per_page=1000&private_token="+creds.gitlab_token,verify=False)
def check_in_directory(email):
    time.sleep(0.02)
    query_res = os.popen('ldapsearch -x -H ldaps://directory.companey.com:636 -b dc=companey,dc=com "(&(mail=%s)(objectClass=person))" | grep -i dn:' % email )
    if len(query_res.read()) >= 2:
        return "yes"
    else:
        return "no"
    query_res.close()

for i in gitlab_res.json():
    if check_in_directory(i["email"]) == "yes":
        helper_string = helper_string + i["email"]+" is alive in Directory and Blocked in Gitlab<br>"

def send_mail(msg_text):
    server = smtplib.SMTP('localhost', 25)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "** Gitlab Blocked Users but Alive in Directoy - "+today_human+" **"
    text = ""
    html = """\
    <html>
      <head></head>
      <body>
        <p>
           %s
        </p>
      </body>
    </html>
    """ %(msg_text)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    server.sendmail("admins@companey.com","other_user@companey.com", msg.as_string())
    server.quit()

send_mail("<font color = green><b><h4> List of blocked users in Gitlab, yet, alive in Directory</h4></b></font><br>"+helper_string)
f = open("gitlab_not_directory.txt", "w+")
f.write(helper_string)
f.close()
