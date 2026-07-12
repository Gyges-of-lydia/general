#!/bin/python
import pexpect
import getpass
import sys
import os
try:
        user=input("Tacacs Username: ")
        password=getpass.getpass("Tacacs Password: ")

        switch_ip = "10.0.0.1"
        switch_un = user
        switch_pw = password


        while True:
                trigger=input("(e)nable ADSM or (d)isable ADSM: ")
                if trigger=="e" or trigger=="E":
                        child = pexpect.spawn('ssh %s@%s' % (switch_un, switch_ip))
                        child.timeout = 4
                        child.logfile = sys.stdout
                        child.expect('password:')
                        child.sendline(switch_pw)
                        i=child.expect(['>', 'Permission denied'])
                        if i==0:
                                child.sendline('enable')
                                child.expect('Password:')
                                child.sendline(switch_pw)
                                child.expect('#')
                                child.sendline('conf t')
                                child.expect('#')
                                child.sendline('http server enable')
                                child.expect('#')
                                child.sendline('http 10.0.0.0 255.255.255.0 inside')
                                child.expect('#')
                                child.sendline('exit')
                                child.expect('#')
                                child.sendline('exit')
                                quit()
                        if i==1:
                                os.system("clear")
                                print("\nWrong Username and/or Password - Can't Proceed, Quitting...")
                                quit(1)

                if trigger=="d" or trigger=="D":
                        child = pexpect.spawn('ssh %s@%s' % (switch_un, switch_ip))
                        child.timeout = 4
                        child.logfile = sys.stdout
                        child.expect('password:')
                        child.sendline(switch_pw)
                        i=child.expect(['>', 'Permission denied'])
                        if i==0:
                                child.sendline('enable')
                                child.expect('Password:')
                                child.sendline(switch_pw)
                                child.expect('#')
                                child.sendline('conf t')
                                child.expect('#')
                                child.sendline('http server enable')
                                child.expect('#')
                                child.sendline('http 10.0.0.0 255.255.0.0 inside')
                                child.expect('#')
                                child.sendline('exit')
                                child.expect('#')
                                child.sendline('exit')
                                quit()
                        if i==1:
                                os.system("clear")
                                print("\nWrong Username and/or Password - Can't Proceed, Quitting...")
                                quit(1)

                else:
                        print("Unknown Option - Try Again:\n")
except  KeyboardInterrupt:
        print("\nPressed Ctrl+C Quitting!")
        quit(1)

