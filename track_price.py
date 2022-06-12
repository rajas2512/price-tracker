from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import datetime
import smtplib
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

url = ' ' #Enter your Amazon's wishlist
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.content,'html.parser')
df = pd.read_csv('wishlist_products.csv')

spans = soup.find_all('span', {'class': 'a-offscreen'})
price = []
for span in spans:
    extract_price = span.text[1:]
    price.append(extract_price)


now = datetime.datetime.now()
df[f'Prices on {now.strftime("%d/%m/%Y")}'] = price


df[f'Prices on {now.strftime("%d/%m/%Y")}'] = df[f'Prices on {now.strftime("%d/%m/%Y")}'].str.replace(',', '').astype(float)


def send_mail():
    sender_email = " " #Enter sender's email
    sender_password = " " #Enter sender's password
    receivers = [" "] #Enter receiver's email addresses
    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header('Price Drop', 'utf-8')), "amazon.price.drop.0@gmail.com"))
    msg['Subject'] = 'Price has reduced'
    message = f'Hey Customer!\nThe price of {product_name} has reduced.\n The difference in the price is {difference}.\n Please visit your wishlist - {url}'
    msg.attach(MIMEText(message))
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receivers, msg.as_string())
    print("Email sent successfully !")
    server.quit()

for i in df.index:
  if (df[f'Prices on {now.strftime("%d/%m/%Y")}'][i] <= df['Desired_Prices'])[i]:
    difference =  df['Desired_Prices'][i] - df[f'Prices on {now.strftime("%d/%m/%Y")}'][i]
    product_name = df.iloc[i][0]
    send_mail()
  else:
    product_name = df.iloc[i][0]
    print(f"The mail will not be sent as the price of {product_name} is not reduced")

df.to_csv('wishlist_products1.csv',index = False)
file1 = 'wishlist_products1.csv'
os.system('start %s' % file1)






