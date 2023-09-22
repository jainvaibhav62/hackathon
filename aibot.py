#!/usr/bin/python3
import imaplib
import email
import re
import ast
import os
import openai
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
import smtplib
from email.utils import formataddr

def receive_email():
    print("receiving email")
    user = os.getenv('GMAIL_USER')
    pswd = os.getenv('GMAIL_PASSWORD')
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    result = imap.login(user, pswd)
    imap.select("INBOX")
    result, data = imap.search(None, '(UNSEEN)')
    for num in data[0].split():
        result, data = imap.fetch(num, '(RFC822)')
        for response in data:
            if isinstance(response, tuple):
                original = email.message_from_bytes(response[1])
                for part in original.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        parsedbody = str(({body.decode("UTF-8")}))
                        parsedbody = re.sub(r'((\\r\\n\s*On\s(Mon|Tue|Wed|Thu|Fri|Sat|Sun))|(\\r\\n\_\_\_\_)).*', '', parsedbody)
                        parsedbody = re.sub(r'(\\r|\\t|\{\')', '', parsedbody)
                        parsedbody = re.sub(r'(\\n\\n|\\n)', ' ', parsedbody)
                newemailfrom = str(original["From"])
                parsedemailfrom = re.findall(r'\<([^\>]*)\>', newemailfrom)
                parsedemailfrom = str(parsedemailfrom[0])
                subject = str(original["Subject"])
                reply = re.search(r'(RE:|Re:|re:)', subject)
                if reply:
                    print("Confirmed reply email")
                else:
                    sys.exit()
                newemailto = str(original["To"])
                parsedaliasto = re.findall(r'^([^\<]*)\s\<', newemailto)
                parsedaliasto = str(parsedaliasto[0])
                parsedemailto = re.findall(r'\<([^\>]*)\>', newemailto)
                parsedemailto = str(parsedemailto[0])
                return(original,parsedaliasto,parsedemailto,subject,parsedbody,parsedemailfrom)

def create_receive_log(parsedemailfrom,parsedemailto,subject,parsedbody):
    logdate = (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")
    parsedbody  = re.sub(r'(\r|\n)',r'', parsedbody)
    log_output = '{"timestamp":"' + logdate + '","action":"receive_phish_response","aiuser":"user","sender":"' + parsedemailfrom + '","recipient":"' + parsedemailto + '","subject":"' + subject + '","body":"' + parsedbody + '"}\n'
    print(log_output)
    l = open("/root/braddev/phishbot.log", "a")
    l.write(log_output)
    l.close

def send_reply(original,parsedaliasto,parsedemailto,parsedemailfrom,subject):
    print("sending reply")
    new = MIMEMultipart("mixed")
    body = MIMEMultipart("alternative")
    aibody,url,phishtype = ai_gen(parsedemailto,parsedemailfrom,subject)
    if phishtype == '1' or phishtype == '2':
        fullbody = '<html><body><br>' + aibody + '<br><br><a href="' + url + '">open Okta</a><br><br> Thank you,<br>' + parsedaliasto + '</body></html>'
    elif phishtype == '3' or phishtype == '4':
        fullbody = '<html><body><br>' + aibody + '<br><br><a href="' + url + '">open Financial Services</a><br><br> Thank you,<br>' + parsedaliasto + '</body></html>'
    body.attach(MIMEText(fullbody, "html"))
    new.attach(body)
    new["Message-ID"] = email.utils.make_msgid()
    new["In-Reply-To"] = original["Message-ID"]
    new["References"] = original["Message-ID"]
    new["Subject"] = original["Subject"]
    new["To"] = original["Reply-To"] or original["From"]
    new['From'] = formataddr(((parsedaliasto), (parsedemailto)))
    new.attach(MIMEMessage(original))
    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    user = os.getenv('GMAIL_USER')
    pswd = os.getenv('GMAIL_PASSWORD')
    s = smtplib.SMTP(smtp_server, smtp_port)
    s.starttls()
    s.login(user, pswd)
    s.sendmail(user, [new["To"]], new.as_string())
    s.quit()
    return(parsedemailfrom,parsedemailto,aibody,subject)

def create_reply_log(parsedemailfrom,parsedemailto,aibody,subject):
    print("creating reply log")
    aibody = re.sub(r'(\r|\n)',r'', aibody)
    logdate = (datetime.now()).strftime("%m/%d/%Y %H:%M:%S")
    log_output = '{"timestamp":"' + logdate + '","action":"send_phish_reply","aiuser":"system","sender":"' + parsedemailto + '","recipient":"' + parsedemailfrom + '","subject":"' + subject + '","body":"' + aibody + '"}\n'
    print(log_output)
    l = open("/root/braddev/phishbot.log", "a")
    l.write(log_output)
    l.close

def ai_gen(parsedemailto,parsedemailfrom,subject):
    print("creating ai reply body")
    aibody = "Reply Body Here"
    url = "https://www.google.com"
    phishtype = '1'
    return(aibody,url,phishtype)

def main():
    original,parsedaliasto,parsedemailto,subject,parsedbody,parsedemailfrom = receive_email()
    create_receive_log(parsedemailfrom,parsedemailto,subject,parsedbody)
    parsedemailfrom,parsedemailto,aibody,subject = send_reply(original,parsedaliasto,parsedemailto,parsedemailfrom,subject)
    create_reply_log(parsedemailfrom,parsedemailto,aibody,subject)

if __name__ == "__main__":
    main()