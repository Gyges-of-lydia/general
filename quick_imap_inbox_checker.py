#!/usr/bin/python
import sys
import imaplib
import os
imap_username = "imap_user"
imap_password = "imap_password"
imap_server = "server.name.com"

def ping(hostname,count):
        count=str(count)
        response = os.system("ping -c "+count+" "+hostname+" > /dev/null")
        if response == 0:
                return True
        else:
                return False


if ping(imap_server,1)==True:
        print "IMAP Server "+ imap_server +" is up"
else:
        print "Server is Down, Quiting.."
        quit()

m=imaplib.IMAP4_SSL(imap_server)
try:
        m.login(imap_user, imap_server)
except imaplib.IMAP4.error:
        print "Login Failed - Quitting..."
        quit()

rl, mailboxes = m.list()
if rl !='OK':
        print "There is a Problem Listing the mail Boxes"
        quit()

ri, data=m.select('Inbox')
if ri=='OK' and data[0]>3:
        print "Mail box is OK"
else:
        print "Mail box Probably Contains more than 3 Messages"
