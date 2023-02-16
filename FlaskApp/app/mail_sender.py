import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'especert54@gmail.com'
email_password = 'xsqskjcawtvuebyx'
#email_receiver = 'elisejohn1995@gmail.com'

# Set the subject and body of the email
subject = 'Alerta Trafico Malicioso Espe-Cert'
body = """
Estimado Usuario
Se ha detectado una amenaza de trafico malicioso, por favor acercarse a la aplicación MT Analizer para mas información.
"""



# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email


def sendMail(email_receiver):
    em = EmailMessage()
    em['From'] = email_sender
    em['Subject'] = subject
    em.set_content(body)
    em['To'] = email_receiver
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())