import smtplib
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPException
import ssl

def login():
    sender = input("Enter sender email: ")
    password = input("Enter app password: ")

    try:
        # Initialize the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls(context=ssl.create_default_context())

        # Log in to the email account
        server.login(sender, password)
        print("Login successful!")

        return sender, password, server

    except SMTPAuthenticationError:
        print("Authentication failed: Incorrect username or password.")
        print("Ensure you are using the correct app password, and check if 2-Step Verification is enabled.")
        return None, None, None
    except SMTPConnectError:
        print("Connection to the SMTP server failed. Check the SMTP settings (server address, port, etc.).")
        return None, None, None
    except TimeoutError:
        print("The connection to the SMTP server timed out. Check your internet connection or try again later.")
        return None, None, None
    except ssl.SSLError:
        print("SSL/TLS error occurred. Make sure your Python environment supports the necessary security protocols.")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        return None, None, None


def info():
    reciepient = input("Recipient email: ")
    subject = input("Subject: ")
    message = input("Message: ")

    text = f"Subject: {subject}\n\n{message}"
    return reciepient, text


def send_email(sender, password, server, reciepient, text):
    try:

        server.sendmail(sender, reciepient, text)
        print("Email sent successfully!")

        server.quit() #close server

    except SMTPException as e:
        print(f"An error occurred while sending the email: {e}")
        if isinstance(e, TimeoutError):
            print("The connection timed out while trying to send the email. Please check your network and try again.")
        elif isinstance(e, SMTPAuthenticationError):
            print("Failed to authenticate with the SMTP server. Please check your credentials.")
        elif isinstance(e, ssl.SSLError):
            print("SSL/TLS error occurred during email sending. Check your environment's security settings.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():

    sender, password, server = login()

    if sender and password and server:

        reciepient, text = info()

        send_email(sender, password, server, reciepient, text)


# Start the application
main()
