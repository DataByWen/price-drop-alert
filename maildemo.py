import requests
from bs4 import BeautifulSoup
import smtplib # part of python's standard lib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText # part of python's standard lib
from email.mime.multipart import MIMEMultipart

load_dotenv()
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
recipient_email = os.getenv("RECIPIENT_EMAIL")
url = os.getenv("PRODUCT_URL")
target_price = int(os.getenv("TARGET_PRICE")) # returns env variables as a string 


def get_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    html_content = BeautifulSoup(r.content, "html.parser")
    content = html_content.find("span", id="span_product_price_sale") # provide html elements to extract data

    # split() based on whitespace and gets stored in a list
    price = content.text.split()[1]
    return round(float(price),2)


def write_mail():
    message = MIMEMultipart("alternative")
    message["Subject"] = "Price Drop Alert"
    message["From"] = email_user
    message["To"] = recipient_email

    # Create the plain-text and HTML version of the message
    text = """\
    An email reminder that the product has dropped to your desired price"""

    html = """\
    <html>
        <body>
            <p>
                his is an email reminder that the product has dropped to your desired price.
            </p>
        </body>
    </html>
    """

    # Turn the string literals into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    return message

    
def send_mail():
    price = get_price()
    print("The price of the product is: ", price)

    if price < target_price:
        email_text = write_mail()
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # Secure connection
            smtp.login(email_user, email_pass)
            smtp.sendmail(email_user, recipient_email, email_text.as_string())
            print("Email successfully sent!")


if __name__ == "__main__":
    send_mail()
