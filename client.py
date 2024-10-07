import socket
import threading
import time
import smtplib
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPException
import ssl
import getpass

# Chatting Variables
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Email Sending Functions
def login():
    sender = input("Enter sender email: ")
    password = getpass.getpass("Enter app password: ")  # Hide the password

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
    recipient = input("Recipient email: ")
    subject = input("Subject: ")
    message = input("Message: ")

    text = f"Subject: {subject}\n\n{message}"
    return recipient, text

def send_email(sender, password, server, recipient, text):
    try:
        server.sendmail(sender, recipient, text)
        print("Email sent successfully!")
        server.quit()  # Close server
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

# Chatting Functions
def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send_chat(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

def receive_chat(client):
    while True:
        try:
            # Receiving messages from the server
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(f"\n{msg}")
                print("Message (q for quit): ", end='', flush=True)
            else:
                break  
        except:
            print("Error receiving data.")
            break

def start_chat():
    answer = input('Would you like to connect to the chat (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    receive_thread = threading.Thread(target=receive_chat, args=(connection,))
    receive_thread.start()

    while True:
        msg = input("Message (q for quit): ")

        if msg == 'q':
            break

        send_chat(connection, msg)

    send_chat(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected from chat')

# Main Menu
def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Start Chat")
        print("2. Send Email")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            start_chat()
        elif choice == '2':
            sender, password, server = login()
            if sender and password and server:
                recipient, text = info()
                send_email(sender, password, server, recipient, text)
        elif choice == '3':
            print("Exiting application.")
            break
        else:
            print("Invalid choice, please try again.")

# Start the Application
main_menu()
