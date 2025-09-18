import socket
import threading
import tkinter as tk

class ChatApp:
    def __init__(self, master):
        self.sock = None

        self.master = master
        master.title("Communication TCP")

        self.frame_top = tk.Frame(master)
        self.frame_top.pack()

        self.role_var = tk.StringVar(value="server")
        tk.Radiobutton(self.frame_top, text="Écouter", variable=self.role_var, value="server").pack(side=tk.LEFT)
        tk.Radiobutton(self.frame_top, text="Se connecter", variable=self.role_var, value="client").pack(side=tk.LEFT)

        self.ip_entry = tk.Entry(self.frame_top)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(side=tk.LEFT)

        self.port_entry = tk.Entry(self.frame_top)
        self.port_entry.insert(0, "12345")
        self.port_entry.pack(side=tk.LEFT)

        self.connect_btn = tk.Button(self.frame_top, text="Lancer", command=self.start_connection)
        self.connect_btn.pack(side=tk.LEFT)

        self.chat_box = tk.Text(master)
        self.chat_box.pack()

        self.msg_entry = tk.Entry(master)
        self.msg_entry.pack(fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

    def start_connection(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        role = self.role_var.get()

        if role == "server":
            threading.Thread(target=self.start_server, args=(port,), daemon=True).start()
        else:
            threading.Thread(target=self.connect_to_server, args=(ip, port), daemon=True).start()

    def start_server(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("", port))
        server.listen(1)
        self.chat_box.insert(tk.END, "Attente de connexion...\n")
        conn, addr = server.accept()
        self.chat_box.insert(tk.END, f"Connecté à {addr}\n")
        self.sock = conn
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def connect_to_server(self, ip, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        self.chat_box.insert(tk.END, f"Connecté à {ip}:{port}\n")
        self.sock = client
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if self.sock and msg:
            self.sock.send(msg.encode())
            self.chat_box.insert(tk.END, f"Moi: {msg}\n")
            self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                self.chat_box.insert(tk.END, f"Reçu: {data.decode()}\n")
            except:
                break

root = tk.Tk()
app = ChatApp(root)
root.mainloop()
