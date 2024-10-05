import threading
import socket
import smtplib
from email.mime.text import MIMEText

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set() 
clients_lock = threading.Lock()  


def send_email(smtp_server, sender_email, sender_password, recipient_email, subject, message):
    try:
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()  # Start TLS for security
            server.login(sender_email, sender_password)  # Login to the SMTP server
            
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


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")

            with clients_lock:
                for c in clients:
                    if c != conn:
                        c.sendall(f"[{addr}] {msg}".encode(FORMAT))
                    else:
                        confirmation_message = f"[SERVER] Your message was successfully sent to other clients."
                        c.sendall(confirmation_message.encode(FORMAT))

    finally:
        with clients_lock:
            clients.remove(conn)  
        conn.close()  


def start():
    print('[SERVER STARTED]! Listening for connections...')
    server.listen()  
    while True:
        conn, addr = server.accept()  
        with clients_lock:
            clients.add(conn) 
        thread = threading.Thread(target=handle_client, args=(conn, addr))  
        thread.start()


start()
