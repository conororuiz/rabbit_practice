import smtplib
import local_settings

types = ['debug','info','warning']

def create_or_open_txt(type, message):
    name=type+'.txt'
    message=message+'\n'
    with open(name,'a+') as f:
      f.write(type+" - "+message)

def send_email(type,msg):
       server = smtplib.SMTP('smtp.gmail.com',587)
       server.ehlo()
       server.starttls()
       server.login(local_settings.EMAIL,local_settings.PASSWORD)
       message= type +" - "+msg
       to='conoro@lsv-tech.com'
       server.sendmail(local_settings.EMAIL, to, message)
       server.quit()

