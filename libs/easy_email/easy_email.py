import smtplib
from email.mime.text import MIMEText

class EasyEmail(object):

    def __init__(self, email_id, email_passwd):
        self.sender_email = email_id
        self.email_context = self.login(email_id, email_passwd)

    #def __del__(self):
    #    self.email_context.quit()

    #465
    def login(self, email_id, email_passwd, host='smtp.gmail.com', port=465 ):
        email_context = smtplib.SMTP_SSL(host,port)
        email_context.ehlo()
        email_context.login(email_id, email_passwd)
        return email_context

    def send(self, target_email, title, contents):
        msg = MIMEText(contents)
        msg['Subject'] = title 
        msg['From'] = self.sender_email 
        msg['To'] = target_email 
        self.email_context.sendmail(self.sender_email, target_email, msg.as_string())

            
if __name__=='__main__':
    email = EasyEmail("goddoe2@gmail.com", "@Tjdwn132")
    email.send("goddoe2@gmail.com","test", "test contents")

