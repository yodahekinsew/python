import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

page = requests.get('http://forecast.weather.gov/MapClick.php?lat=42.3587&lon=-71.0567#.WnRSs6inHIU')
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id = 'seven-day-forecast')
forecast_items = seven_day.find_all(class_='tombstone-container')
tonight = forecast_items[0]
forecast = tonight.find_all('p')[1]
real_forecast = forecast.find('img')
real = real_forecast['title']

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login('yodahekinsew@gmail.com', 'Kinsew12')


message = real

msg = MIMEMultipart()
msg['From'] = 'yodahekinsew@gmail.com'
msg['To'] = 'yodahekinsew@gmail.com'
msg['Subject']='Python Weather'
msg.attach(MIMEText(message,'plain'))

s.send_message(msg)
