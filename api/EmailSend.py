import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, message):
    # Create an instance of the SMTP server
    smtp_password = "gycc qxbp tqts umbk"
    smtp_username = "tarek6221@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Port may vary depending on the SMTP server
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start a TLS encrypted session

    # Log in to the SMTP server
    server.login(smtp_username, smtp_password)

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Send the email
    server.sendmail(smtp_username, to_email, msg.as_string())
    print("hebhoub")
    # Quit the SMTP server
    server.quit()

# # Example usage:
# to_email = "hebhoubtarekziad@gmail.com"
# subject = "Hello from Python!"
# message = "This is a test email sent from a Python function."



# send_email(to_email, subject, message)