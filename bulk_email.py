# https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
# https://docs.python.org/2/library/email-examples.html
# you have to allow less secure apps in gmail from here:
# https://myaccount.google.com/lesssecureapps

import smtplib
from email.mime.text import MIMEText

gmail_user = 'example@gmail.com'
gmail_pwd = ''  # hardcode your password
subject = 'Subject'


def update_msg(to, msg):
    # make personalised messages
    return msg


def send_email(to, msg):
    # Prepare actual message
    msg = update_msg(to, msg)
    msg = MIMEText(msg)
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_user, to,  msg.as_string())
        server.close()
        print('sent to %s' % to)
    except:
        with open('toSend.txt', 'a') as f:
            f.write(to + '\n')
        print('Not sent to %s' % to)


def main():

    with open('msg_body.txt', 'r') as f:
        msg = f.read()

    with open('test_email_list.txt', 'r') as f:
        for email in f.readlines():
            send_email(email, msg)


if __name__ == '__main__':
    main()
