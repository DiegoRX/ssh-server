import os
import socket
import threading
import paramiko

# Ruta donde se guardarán los archivos recibidos
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Clave privada del servidor (genera una con `ssh-keygen`)
HOST_KEY = paramiko.RSAKey(filename="server_key")

class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        print(f"Intento de inicio de sesión - Usuario: {username}, Contraseña: {password}")
        if username == "admin" and password == "password":
            print("Autenticación exitosa.")
            return paramiko.AUTH_SUCCESSFUL
        print("Autenticación fallida.")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

def handle_client(client_socket):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(HOST_KEY)
    server = SSHServer()

    try:
        transport.start_server(server=server)
        channel = transport.accept(20)
        if channel is None:
            print("No se pudo establecer el canal SSH.")
            return

        print("Cliente conectado.")

        # Recibir el archivo XML con progreso
        file_data = b""
        total_received = 0
        chunk_size = 1024  # Tamaño del fragmento (bytes)
        print("Recibiendo archivo...")
        while True:
            data = channel.recv(chunk_size)
            if not data:  # El cliente ha cerrado la conexión de escritura
                break
            file_data += data
            total_received += len(data)
            print(f"Progreso: {total_received} bytes recibidos", end="\r")

        print("\nArchivo recibido completamente.")

        # Guardar el archivo XML
        file_name = f"{UPLOAD_DIR}/received_file.xml"
        with open(file_name, "wb") as f:
            f.write(file_data)
        print(f"Archivo XML guardado como {file_name}")

        # Enviar confirmación al cliente
        try:
            channel.send("Archivo recibido correctamente.")
        except Exception as e:
            print(f"No se pudo enviar la confirmación al cliente: {e}")

    except Exception as e:
        print(f"Error durante la conexión: {e}")
    finally:
        try:
            channel.close()
        except Exception:
            pass
        transport.close()

def start_ssh_server(host="0.0.0.0", port=2222):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor SSH iniciado en {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Nueva conexión desde {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_ssh_server()