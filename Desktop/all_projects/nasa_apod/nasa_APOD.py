import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import requests ##error comes sometimes
import time
from io import BytesIO

def fetch_apod():

    api_key = "KEY" 
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"# NASA APOD API and key

    response = requests.get(url)
    data = response.json()

    if data.get("media_type") != "image":
        raise ValueError("The APOD today is not an image.")

    image_url = data['url']
    image_response = requests.get(image_url)
    image_data = image_response.content

    return image_data

def send_email_with_image(image_data, receiver_emails, num_times, delay):
    sender_email = "XXX@gmail.com"
    password = "USE APP PASS, NOT regular one, as GMAIL restricts"  

    for i in range(num_times):
        for receiver_email in receiver_emails:
            # Creation of a multipart message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Astronomy Picture of the Day"

            
            body = "The Astronomy Picture of the Day is attached."
            msg.attach(MIMEText(body, 'plain'))

            # Attaching of the image
            image_part = MIMEImage(image_data)
            image_part.add_header('Content-Disposition', 'attachment; filename="apod_image.jpg"')
            msg.attach(image_part)

            # SMTP server and sending email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print(f"Email {i + 1} sent to {receiver_email} successfullyyyy!!!")

        # delayyy
        time.sleep(delay)

# Fetch image from NASA APOD
try:
    image_data = fetch_apod()
except Exception as e:
    print(f"Error fetching APOD: {e}")
    exit(1)

receiver_emails = ["xxx@yahoo.com"]

num_times = 2
delay = 10

send_email_with_image(image_data, receiver_emails, num_times, delay)