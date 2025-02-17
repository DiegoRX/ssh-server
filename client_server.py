import paramiko
from tqdm import tqdm

# Configuración del cliente
HOST = "127.0.0.1"  # Dirección local
PORT = 2222
USERNAME = "admin"
PASSWORD = "password"
FILE_PATH = "archivo.xml"  # Ruta del archivo que deseas enviar

try:
    # Leer el archivo XML
    with open(FILE_PATH, "rb") as f:
        file_data = f.read()

    # Conectar al servidor SSH
    transport = paramiko.Transport((HOST, PORT))
    transport.connect(username=USERNAME, password=PASSWORD)

    # Abrir un canal SSH
    channel = transport.open_session()

    print("Enviando archivo...")

    # Enviar el archivo XML con progreso
    chunk_size = 1024  # Tamaño del fragmento (bytes)
    total_size = len(file_data)
    with tqdm(total=total_size, unit="B", unit_scale=True, desc="Progreso") as pbar:
        for i in range(0, total_size, chunk_size):
            chunk = file_data[i:i + chunk_size]
            channel.send(chunk)
            pbar.update(len(chunk))

    # Indicar al servidor que la transmisión ha terminado
    channel.shutdown_write()  # Indica que no se enviarán más datos
    print("\nArchivo enviado completamente.")

    # Recibir la confirmación del servidor
    response = channel.recv(1024).decode()
    print(f"Respuesta del servidor: {response}")

except Exception as e:
    print(f"Error durante la conexión: {e}")
finally:
    # Cerrar la conexión
    try:
        channel.close()
    except Exception:
        pass
    transport.close()