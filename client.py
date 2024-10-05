import socket
import time
import threading
import smtplib
from email.mime.text import MIMEText

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

def receive(client):
    while True:
        try:
            # Receiving messages from the server
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(f"\n{msg}")
                print("Message (q for quit): ", end='', flush=True)
            else:
                break  
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def send_email(sender_email, sender_password, recipient_email, subject, message):
    smtp_server = 'smtp.yourdomain.com'  # replace with your SMTP server
    try:
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email sent to {recipient_email} from {sender_email}")
    except smtplib.SMTPAuthenticationError:
        print("Authentication Failure: Check your email and password.")
    except smtplib.SMTPConnectError:
        print("Error connecting to the SMTP server.")
    except Exception as e:
        print(f"An error occurred: {e}")

def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect() 
    receive_thread = threading.Thread(target=receive, args=(connection,))  
    receive_thread.start()

    while True:
        msg = input("Message (q for quit): ")
        if msg == 'q':
            break

        # Sending email
        send_email('your_email@example.com', 'your_password', 'recipient@example.com', 'Subject', msg)
        send(connection, msg)  

    send(connection, DISCONNECT_MESSAGE)  
    time.sleep(1)
    print('Disconnected')

start()
