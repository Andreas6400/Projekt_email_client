import smtplib, ssl
from pathlib import Path

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Webscrapen --> Seite aus Internet in Email fügen
def parseSourceCode(my_url):
    hdr = {'User-Agent': 'Mozilla/5.0'} #Header-Parameter
    req = Request(my_url,headers=hdr) #URL unter Verwendung der angegebenen Header-Parameter anfordern
    uClient = urlopen(req) #Öffnen Sie die angeforderte URL
    page_html = uClient.read() #Inhalt der Seite lesen
    uClient.close()
    return BeautifulSoup(page_html, "html.parser") #Code mit BeautifulSoup analysieren

# <----------EMAIL SECTION---------->

def emailSenden():
    # Definition der Sender-, Empfängeremail und Passwort
    sender_email = "Sender Email eingeben"
    empfaenger_email = "Empfänger Email eingeben"
    password = input("Gebe dein Passwort ein und drücke Enter: ")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Bundesligatabelle" #Betreff
    message["From"] = sender_email #Senderemail
    message["To"] = empfaenger_email #Empfängeremail

    # Erstellen von Text- und HTML-Version Ihrer Nachricht
    # Textteil Beginn
    text = """\
    Hi,
    Hier wird die Bundeligatabelle ausgegeben?"""
    # Textteil Ende
    # HTML Beginn
    html = ("""\
    <html>
        <head>
            <link rel="stylesheet" type="text/css" href="https://www.bundesliga.com/styles.2fdeb84b18a8916693ae.css">
        </head>
        <body>
            <h1>Die neuste Bundesligatabelle</h1>
            """
            +str(tabelle)+ 
            """
        </body>
    </html>
    """)
    # HTML Ende

    # Vewandle in Text und HTML um
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Fügen Sie der MIMEMultipart-Nachricht HTML- / Text-Teile hinzu
    # Der E-Mail-Client versucht zuerst, den letzten Teil zu erstellen
    message.attach(part1)
    message.attach(part2)

    #---Stellen Sie eine sichere Verbindung zum Server her und senden Sie eine E-Mail---

    #Verwenden Sie ihren E-Mail-Anbieter mit Port HIER GEWUENSCHTEN SMTP RAUSSUCHEN
    session = smtplib.SMTP('Email-Anbieter eingeben', "Port") # Neuer Port und Email-Anbieter eingeben
    session.starttls() #Sicherheit aktivieren
    session.login(sender_email, password) #Login mit Mail-ID und Passwort
    text = message.as_string()
    session.sendmail(sender_email, empfaenger_email, text)
    session.quit()
    print("Mail sent!") # Konsole zeigt das Email versandt wurde

bundesliga_source = parseSourceCode("https://www.bundesliga.com/de/bundesliga/tabelle")
tabelle = bundesliga_source.find("div", {"class": "container tablepage-container"})

# Bestimmter Zeitpunkt wenn 1. Platz ändert
#
body = bundesliga_source.find("tbody") # sucht den Abschnitt tbody und speichert in der Variable body
erster = body.find("span", {"class": "d-none d-lg-inline"})# sucht in dem body nach dem span mit der angegebnen class
path = Path("ersterPlatz.txt")
if path.is_file(): # Prüfung ob es die Datei existiert 
    with open("ersterPlatz.txt","r+") as datei: # Öffnen von Datei
        bisherigerErster = datei.read() # lese den Inhalt der Datei uns speichert in Variable 
        if bisherigerErster == str(erster.contents): # Prüfe ob Inhalt der Datei mit dem Inhalt der Website übreinstimmmt
            print("Nichts neues!") # Ausgabe wenn sich der 1. Platz nicht ändert
            exit() # Programm beenden
        else:
            datei.write(str(erster.contents)) # Überschreiben der Datei mit dem neuen ersten Platz
            datei.close() # Datei schließen und speichern
            emailSenden() # Die Funktion emailSenden wird aufgerufen und durch geführt
else:
    with open("ersterPlatz.txt","w") as datei: # Erstellen einer Datei
        datei.write(str(erster.contents)) # Schreibe den 1. Platz rein
        datei.close() # Schließe und speichere die Datei
        emailSenden() # Die Funktion emailSenden wird aufgerufen und durch geführt