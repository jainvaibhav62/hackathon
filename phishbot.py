#!/usr/bin/python3
import argparse
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import time
from datetime import datetime
import os

class colors:
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'

def initialize():
    parser = argparse.ArgumentParser("phishbot operators")
    parser.add_argument("-e", "--email", type=str, help="enter email of recipient")
    parser.add_argument("-f", "--file", type=str, help="enter file with list of recipients")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    email = args.email
    file = args.file
    return(email,file)

def single_phish(email):
    logo_gen()
    user,mail_server = mail_server_connect()
    url = create_url()
    email_from, email_to, subject, url, body = send_email(user,email,mail_server,url)
    create_log(email_from, email_to, subject, url, body)
    mail_server.quit()

def multi_phish(file):
    logo_gen()
    print(colors.GREEN + "Starting multi target phish using file " + file + " \n" + colors.ENDC)
    user,mail_server = mail_server_connect()
    email_list = open(file, 'r')
    emails = email_list.readlines()
    for email in emails:
        url = create_url()
        email_from, email_to, subject, url, body = send_email(user, email, mail_server, url)
        create_log(email_from, email_to, subject, url, body)
        time.sleep(1)
    mail_server.quit()
    email_list.close()

def logo_gen():
    print(colors.YELLOW + "                           __    _      __    __          __")
    print(colors.YELLOW + " __                 ____  / /_  (_)____/ /_  / /_  ____  / /_")
    print(colors.YELLOW + "/o \\/    __        / __ \\/ __ \\/ / ___/ __ \\/ __ \\/ __ \\/ __/")
    print(colors.YELLOW + "\\__/\\   /o \\/     / /_/ / / / / (__  ) / / / /_/ / /_/ / /_  ")
    print(colors.YELLOW + "        \\__/\\    / .___/_/ /_/_/____/_/ /_/_.___/\\____/\\__/  ")
    print(colors.YELLOW + "                /_/ ")

def mail_server_connect():
    user = os.getenv('OUTLOOK_USER')
    pswd = os.getenv('OUTLOOK_PASSWORD')
    smtp_port = 587
    smtp_server = "smtp-mail.outlook.com"
    print(colors.GREEN + "Connecting to mail server ... " + colors.ENDC)
    mail_server = smtplib.SMTP(smtp_server, smtp_port)
    mail_server.starttls()
    mail_server.login(user, pswd)
    print(colors.GREEN + "Connected to mail server ... \n" + colors.ENDC)
    return(user,mail_server)

def send_email(user,email,mail_server,url):
    print(colors.GREEN + " <>< <><  Sending Phishbot email to " + email + "  <>< <>< " + colors.ENDC)
    email_from = user
    email_to = email
    subject = "Organizational Announcement"
    body = '<h2>We are pleased to welcome John Haxor to the organization! </h2><br /><br />' \
           '<a href="' + url + '">Please check his linkedin profile</a><br /><br />' \
           '<body>Regards,<br />Jane Doe<br />' \
           '<style="color: #FF0000;"><b>Spyder Financial Services</b><br />'
    msg = MIMEMultipart()
    msg['From'] = formataddr(('John Marshal', email_from))
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    ##uncomment below section if attachment required
    #filename = "/Users/radspyder/Downloads/spider.png"
    #attachment = open(filename, 'rb')
    #attachment_package = MIMEBase('application', 'octet-stream')
    #attachment_package.set_payload((attachment).read())
    #encoders.encode_base64(attachment_package)
    #attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    #msg.attach(attachment_package)
    ##end of attachment section
    text = msg.as_string()
    print(colors.GREEN + "<>< <><  Successfully sent Phishbot email to " + email_to + "  <>< <>< \n" + colors.ENDC)
    mail_server.sendmail(email_from, email_to, text)
    return(email_from, email_to, subject, url, body)

def create_url():
    print(colors.GREEN + "Creating unique url for target ... " + colors.ENDC)
    t = str(round(time.time()))
    f = open("/var/www/html/" + t + ".html", "w")
    f.write("<html>gotcha!</html>")
    f.close
    url = "http://44.209.233.111/" + t + ".html" ###update IP address/hostname
    print(colors.GREEN + "Created url " + url + " \n" + colors.ENDC)
    return(url)

def create_log(email_from,email_to,subject,url,body):
    print(colors.GREEN + "Create log entry ... \n" + colors.ENDC)
    logdate = (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")
    log_output = logdate + ' action="send_phish" sender="' + email_from + '" recipient="' + email_to + '" subject="' + subject + '" attachment= phishurl="' + url + '" body="' + body + '"\n'
    l = open("/opt/hackathon/phishbot.log", "a")
    l.write(log_output)
    l.close

email,file = initialize()
if email:
    single_phish(email)
if file:
    multi_phish(file)