import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
import os

month_day_year = "%B %d %Y"
before_day = datetime.strptime("March 20 2017", month_day_year)

# go grab the XML file from the French consulate server

cookies = {
    'JSESSIONID': '91C3CAD261C01A33B86B574930381827.jvm01912-3',
}

headers = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8,ja;q=0.6,fr;q=0.4',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://pastel.diplomatie.gouv.fr/rdvinternet/html-3.04.03/frameset/bodyFrame.html',
    'Connection': 'keep-alive',
}

response = requests.get('https://pastel.diplomatie.gouv.fr/rdvinternet/flux/protected/RDV/prise/horaires.xml', headers=headers, cookies=cookies)

# Parse the XML into something useful
soup = BeautifulSoup(response.text, 'lxml')

earliest_date_text = soup.find("ho").find("d").string
earliest_date = datetime.strptime(earliest_date_text, '%d%m%Y')

# Check if we should notify Teo and email him if he hasn't been notified already
log_prefix = datetime.now().strftime("%I:%M %p on %B %d, %Y") + "  :  "

if (before_day - earliest_date).days >= 0:
    new_date_description = earliest_date.strftime(month_day_year)
    log_prefix += "Found something on " + new_date_description + ". "

    # Oh boy! Email him immediately!
    # (but only if we haven't emailed him before...)
    sent_email_path = "/tmp/have_sent_email"
    if os.path.isfile(sent_email_path):
        print log_prefix + "Already sent an email so hold off..."
    else:
        print log_prefix + "Sending an email now!"
        from_address = ""
        to_address  = ""
        email_password = ""

        # I could make a file type with these as three lines but I already made
        # the README so deal with it.
        with open("/tmp/from_address.txt", "r") as secret_file:
            from_address = secret_file.readlines()[0].strip()
        with open("/tmp/to_address.txt", "r") as secret_file:
            to_address = secret_file.readlines()[0].strip()
        with open("/tmp/email_password.txt", "r") as secret_file:
            email_password = secret_file.readlines()[0].strip()

        email_message = "\r\n".join([
          "From: " + from_address,
          "To: " + to_address,
          "Subject: New French Consulate appointment available!",
          "",
          "It's on " + new_date_description,
          "",
          "Click here to book " +
          "https://pastel.diplomatie.gouv.fr/rdvinternet/html-3.04.03/frameset/frameset.html?lcid=1&sgid=260&suid=1",
        ])

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(from_address, email_password)
        server.sendmail(from_address, to_address, email_message)
        server.quit()

        # write to a temp file so we don't send 5000 emails
        open(sent_email_path, 'a').close()
else:
    print log_prefix + "Nothing before " + before_day.strftime(month_day_year)
