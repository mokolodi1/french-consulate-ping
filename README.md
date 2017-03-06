# Ping the French Consulate for cancellations

Being American, I need a visa to go to 42 in Paris.

I created this script to ping the French consulate's website for creating an appointment to notify me of any cancellations.

## Setup

```
# create a couple temp files with email information
echo "myemail@gmail.com" > /tmp/to_email.txt
echo "notifyemail@gmail.com" > /tmp/from_email.txt
echo "MyEmailPassword" > /tmp/email_password.txt

# clone this repo
cd ~
git clone https://github.com/mokolodi1/french-visa-appointment-ping

# set up cron to run it every 5 minutes
(crontab -l ; echo "*/5 * * * * python ~/ping_appointment.py > ~/ping_logs.txt")| crontab -
```
