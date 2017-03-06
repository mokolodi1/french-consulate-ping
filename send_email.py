import smtplib

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
  "From: " + from_email,
  "To: " + to_email,
  "Subject: New appointment available!",
  "",
  "Wow isn't this cool!"
  ])

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(from_address, email_password)
server.sendmail(from_address, to_address, email_message)
server.quit()
