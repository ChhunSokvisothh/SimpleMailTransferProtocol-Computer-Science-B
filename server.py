import threading
import socket
import smtplib

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set() 
clients_lock = threading.Lock()  

def send_email(sender, password, recipient, subject, message):
    try:
        # Set up the server
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()

        # Log in to the email account
        smtp_server.login(sender, password)

        # Create the email message
        email_message = f"Subject: {subject}\n\n{message}"

        # Send the email
        smtp_server.sendmail(sender, recipient, email_message)
        smtp_server.quit()

        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

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

            data = msg.split(",")
            if len(data) == 5:
                sender, recipient, subject, message, password = data
                email_sent = send_email(sender, password, recipient, subject, message)

                if email_sent:
                    confirmation_message = "Email sent successfully!"
                else:
                    confirmation_message = "Failed to send email."
                
                #confirmation
                conn.sendall(confirmation_message.encode(FORMAT))
            else:
                #Broadcast the chat
                with clients_lock:
                    for c in clients:
                        if c != conn:
                            c.sendall(f"[{addr}] {msg}".encode(FORMAT))

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
