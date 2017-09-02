# coding=utf-8
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import pandas as pd

pd.set_option('display.max_colwidth', -1)

print "Starting the mailing process... Time: {}\n\n\n".format(datetime.datetime.now())
with open('bakeka_new.msg', 'rb') as f:
    new_df = pd.read_msgpack(f.read())
'''
head = new_df.head(2)
print head

head['link'] = head['link'].apply(lambda x: '<a href="{}">link</a>'.format(x))
table = head.to_html(escape=False)
'''

new_df['link'] = new_df['link'].apply(lambda x: '<a href="{}">link</a>'.format(x))
table = new_df.to_html(escape=False)

html_table = """\
<html>
  <head></head>
  <body>
  <h1>RoomaMI... ci pensa la stanza a trovare te!</h1>
  	<p1>Ecco gli ultimi annunci pubblicati su Bakeka:<br></p1>
    <br>
    {}
  </body>
</html>
""".format(table.encode('utf-8'))


fromaddr = "andrea.ricca91@gmail.com"
toaddr  = "andrea.ricca@hotmail.it"
pwd = "01557452A+"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "RoomaMI! Ecco i nuovi annunci per la tua ricerca"

#body = "RoomaMI... ci pensa la stanza a trovare te!\nEcco un esempio di risultato: \n"
#msg.attach(MIMEText(body, 'plain'))
msg.attach(MIMEText(html_table, 'html'))
#print msg

print "Sending...\n\n"

server = smtplib.SMTP('smtp.gmail.com', 587, timeout=120)
server.ehlo()
server.starttls()
server.login(fromaddr, pwd)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
print "Sent!\n"
print "Mailing process ended.\n"
''''''