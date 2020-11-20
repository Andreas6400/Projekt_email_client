import smtplib, ssl

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def parseSourceCode(my_url):
    hdr = {'User-Agent': 'Mozilla/5.0'} #Header-Parameter
    req = Request(my_url,headers=hdr) #URL unter Verwendung der angegebenen Header-Parameter anfordern
    uClient = urlopen(req) #Öffnen Sie die angeforderte URL
    page_html = uClient.read() #Inhalt der Seite lesen
    uClient.close()
    return BeautifulSoup(page_html, "html.parser") #Code mit BeautifulSoup analysieren

bundesliga_source = parseSourceCode("https://www.bundesliga.com/de/bundesliga/tabelle")

tabelle = bundesliga_source.find("div", {"class": "container tablepage-container"})


# <----------EMAIL SECTION---------->

# Definition der Sender-, Empfängeremail und Passwort
sender_email = "andreas@brossmerhoehe.de"
empfaenger_email = "andreas@brossmerhoehe.de"
password = input("Gebe dein Passwort ein und drücke Enter: ")

message = MIMEMultipart("alternative")
message["Subject"] = "Bundesligatabelle" #Betreff
message["From"] = sender_email #Senderemail
message["To"] = empfaenger_email #Empfängeremail

# Erstellen von Text- und HTML-Version Ihrer Nachricht
text = """\
Hi,
Hier wird die Bundeligatabelle ausgegeben?"""
html = ("""\
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="https://www.bundesliga.com/styles.2fdeb84b18a8916693ae.css">
    </head>
    <body>
        <h1>Bundesligatabelle</h1>
        """
        +str(tabelle)+ 
        """
    </body>
</html>
""")

# Vewandle in Text und HTML um
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Fügen Sie der MIMEMultipart-Nachricht HTML- / Text-Teile hinzu
# Der E-Mail-Client versucht zuerst, den letzten Teil zu erstellen
message.attach(part1)
message.attach(part2)

#---Stellen Sie eine sichere Verbindung zum Server her und senden Sie eine E-Mail---

#Verwenden Sie ihren E-Mail-Anbieter mit Port HIER GEWUENSCHTEN SMTP RAUSSUCHEN
session = smtplib.SMTP('smtp.brossmerhoehe.de', 25) 
session.starttls() #Sicherheit aktivieren
session.login(sender_email, password) #Login mit Mail-ID und Passwort
text = message.as_string()
session.sendmail(sender_email, empfaenger_email, text)
session.quit()
print("Mail sent!")
