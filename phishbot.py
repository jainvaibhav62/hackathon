#!/usr/bin/python3
import sys
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import openai
import shutil
import time
from datetime import datetime

class colors:
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BOLD = '\033[1m'
    RED = '\033[31m'

def logo():
    print(colors.BOLD + colors.YELLOW + "\n                           __    _      __    __          __")
    print(" __                 ____  / /_  (_)____/ /_  / /_  ____  / /_")
    print("/o \\/    __        / __ \\/ __ \\/ / ___/ __ \\/ __ \\/ __ \\/ __/")
    print("\\__/\\   /o \\/     / /_/ / / / / (__  ) / / / /_/ / /_/ / /_  ")
    print("        \\__/\\    / .___/_/ /_/_/____/_/ /_/_.___/\\____/\\__/  ")
    print("                /_/ \n" + colors.ENDC)

def menu():
    print(colors.ENDC + colors.BOLD + "Select an option to begin:\n")
    print("  1) Single Target Email Phish -> Employee")
    print("  2) Multi Target Email Phish -> Employees")
    print("  3) Single Target Email Phish -> Customer")
    print("  4) Multi Target Email Phish -> Customers\n")
    print("  Press any other key to exit...\n")
    input1 = input("> ")
    if input1 == '1' or input1 == '3':
        print("\nStarting single target phish -> Employee\n")
        input2 = input(colors.ENDC + colors.BOLD + "Enter Target email address: " + colors.ENDC)
        input3 = input(colors.ENDC + colors.BOLD + "Enter Sender Alias (ex. John Doe): " + colors.ENDC)
        if input1 == '1':
            confirm = input(colors.GREEN + colors.BOLD + "\nExecute single target phish to Employee: " + input2 + " with Sender Alias: " + input3 + " . Press \"y\" to confirm, press any other key to exit.\n> " + colors.ENDC)
            if confirm == 'y' or confirm == 'Y':
                return(input1, input2, input3)
            else:
                print(colors.RED + colors.BOLD + "\nExiting...\n" + colors.ENDC)
                sys.exit()

        elif input1 == '3':
            confirm = input(colors.GREEN + colors.BOLD + "\nExecute single target phish to Customer: " + input2 + " with Sender Alias: " + input3 + " . Press \"y\" to confirm, press any other key to exit.\n> " + colors.ENDC)
            if confirm == 'y' or confirm == 'Y':
                return(input1, input2, input3)
            else:
                print(colors.RED + colors.BOLD +"\nExiting...\n" + colors.ENDC)
                sys.exit()
    elif input1 == '2' or input1 == '4':
        print("\nStarting multi target phish -> Employees\n")
        input2 = input(colors.ENDC + colors.BOLD + "Enter path to file of email addresses for multi target phish (ex. /home/user/list.csv): " + colors.ENDC)
        input3 = input(colors.ENDC + colors.BOLD + "Enter Sender Alias (ex. John Doe): " + colors.ENDC)
        if input1 == '2':
            confirm = input(colors.GREEN + colors.BOLD + "\nExecute multi target phish to Employees in file: " + input2 + " with Sender Alias: " + input3 + " . Press \"y\" to confirm, press any other key to exit.\n> " + colors.ENDC)
            if confirm == 'y' or confirm == 'Y':
                return(input1, input2, input3)
            else:
                print(colors.RED + colors.BOLD + "\nExiting...\n" + colors.ENDC)
                sys.exit()
        elif input1 == '4':
            confirm = input(colors.GREEN + colors.BOLD + "\nExecute multi target phish to Customers in file: " + input2 + " with Sender Alias: " + input3 + " . Press \"y\" to confirm, press any other key to exit.\n> " + colors.ENDC)
            if confirm == 'y' or confirm == 'Y':
                return(input1, input2, input3)
            else:
                print(colors.RED + colors.BOLD + "\nExiting...\n" + colors.ENDC)
                sys.exit()
    else:
        print(colors.RED + colors.BOLD + "\nExiting...\n" + colors.ENDC)
        sys.exit()

def single_phish(input1, input2, input3):
    user,mail_server = mail_server_connect()
    email_to = input2
    send_email(user,mail_server,email_to,input1,input2,input3)
    mail_server.quit()

def multi_phish(input1, input2, input3):
    user,mail_server = mail_server_connect()
    try:
        email_list = open(input2, 'r')
    except:
        print(colors.RED + colors.BOLD + "file not found... Exiting...\n" + colors.ENDC)
        mail_server.quit()
        sys.exit()
    print("Starting multi phish")
    emails = email_list.readlines()
    for email in emails:
        email_to = email.rstrip('\n')
        send_email(user,mail_server,email_to,input1,input2,input3)
        time.sleep(1)
    mail_server.quit()

def mail_server_connect():
    user = os.getenv('GMAIL_USER')
    pswd = os.getenv('GMAIL_PASSWORD')
    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    print(colors.ENDC + colors.BOLD + "\nConnecting to mail server ... " + colors.ENDC)
    mail_server = smtplib.SMTP(smtp_server, smtp_port)
    mail_server.starttls()
    mail_server.login(user, pswd)
    return(user,mail_server)

def ai_gen(input1):
    if input1 == '1' or input1 == '2':
        subject = "Employee Subject"
        body = "Employee Body"
    elif input1 == '3' or input1 == '4':
        subject = "Customer Subject"
        body = "Customer Body"
    print(colors.ENDC + colors.BOLD + "AI Generating email subject and body...")
    return(subject,body)

def send_email(user,mail_server,email_to,input1,input2,input3):
    subject,body = ai_gen(input1)
    url = url_gen(input1)
    print(colors.GREEN + colors.BOLD + " <>< <><  Sending Phishbot email to " + email_to + " with email Alias " + input3 + " <>< <>< " + colors.ENDC)
    email_from = user
    if input1 == '1' or input1 == '2':
        fullbody = '<html><body><br>' + body + '<br><br><a href="' + url + '">open Okta</a><br><br> Thank you,<br>' + input3 + '</body></html>'
    if input1 == '3' or input1 == '4':
        fullbody = '<html><body><br>' + body + '<br><br><a href="' + url + '">open Financial Services</a><br><br> Thank you,<br>' + input3 + '</body></html>'
    msg = MIMEMultipart()
    msg['From'] = formataddr((input3, email_from))
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(fullbody, 'html'))
    text = msg.as_string()
    mail_server.sendmail(email_from, email_to, text)
    create_log(email_from, email_to, subject, url, body, input1)
    return(email_from, email_to, subject, body)

def url_gen(input1):
    t = str(round(time.time()))
    if input1 == '1' or input1 == '2':
        src_file = "/root/braddev/file.html"
        dst_file = "/var/www/html/" + t + "_okta"
        url = "http://44.209.233.111/" + t + "_okta"
    elif input1 == '3' or input1 == '4':
        src_file = "/root/braddev/file.html"
        dst_file = "/var/www/html/" + t + "_toyotafinancial"
        url = "http://44.209.233.111/" + t + "_toyotafinancial"
    shutil.copy(src_file,dst_file)
    print(colors.ENDC + colors.BOLD + "Creating target url: " + url + " ..." + colors.ENDC)
    return(url)

def create_log(email_from,email_to,subject,url,body,input1):
    print(colors.ENDC + colors.BOLD + "Create log entry ... \n" + colors.ENDC)
    body = re.sub(r'(\r|\n)',r'', body)
    logdate = (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")
    log_output = '{"timestamp":"' + logdate + '","phishtype":"' + input1 + '","action":"send_initial_phish","aiuser":"system","sender":"' + email_from + '","recipient":"' + email_to + '","subject":"' + subject + '","phishurl":"' + url + '","body":"' + body + '"}\n'
    l = open("/opt/hackathon/phishbot.log", "a")
    l.write(log_output)
    l.close

def main():
    logo()
    input1, input2, input3 = menu()
    if input1 == '1' or input1 == '3':
        single_phish(input1, input2, input3)
    if input1 == '2' or input1 == '4':
        multi_phish(input1, input2, input3)

if __name__ == "__main__":
    main()