import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    GMAIL_SMTP = "smtp.gmail.com"
    GMAIL_IMAP = "imap.gmail.com"

    def __init__(self, send_email, password, subject, recipients, message, header):
        self.send_email = send_email
        self.password = password
        self.subject = subject
        self.recipients = recipients
        self.message = message
        self.header = header
        return

    def Send_message(self):
        msg = MIMEMultipart()
        msg['From'] = self.send_email
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))
        ms = smtplib.SMTP(self.GMAIL_SMTP, 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()
        ms.login(self.send_email, self.password)
        ms.sendmail(self.send_email, ms, msg.as_string())
        ms.quit()
        return

    def Recieve_message(self):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.send_email, self.password)
        mail.list()
        mail.select('inbox')
        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    a = Email('login@gmail.com', 'qwerty', 'Subject', ['vasya@email.com', 'petya@email.com'], 'Message', header=None)
    print(Email.Send_message())
    print(Email.Recieve_message())