Aquí tienes una documentación completa en formato Markdown (`.md`) para el servidor SSH que hemos desarrollado. Esta documentación incluye una descripción general, instrucciones de instalación, configuración, uso y solución de problemas.

---

# Documentación del Servidor SSH para Recepción de Archivos

## **Descripción General**

Este servidor SSH está diseñado para recibir archivos de forma segura a través de una conexión SSH. Utiliza la biblioteca `paramiko` para manejar las conexiones SSH y permite a los clientes enviar archivos al servidor. El servidor muestra el progreso del envío tanto en el lado del cliente como en el lado del servidor.

El servidor es ideal para entornos donde se necesita transferir archivos de forma segura entre sistemas locales o remotos.

---

## **Requisitos Previos**

### **1. Dependencias**
- Python 3.x
- Bibliotecas Python:
  - `paramiko`: Para manejar las conexiones SSH.
  - `tqdm`: Para mostrar una barra de progreso visualmente atractiva.

Instala las dependencias con el siguiente comando:

```bash
pip install paramiko tqdm
```

### **2. Clave Privada**
El servidor requiere una clave privada RSA para autenticar las conexiones SSH. Puedes generarla con el siguiente comando:

```bash
ssh-keygen -t rsa -b 4096 -f server_key -N ""
```

Esto generará dos archivos:
- `server_key`: La clave privada.
- `server_key.pub`: La clave pública (no es necesaria para este servidor).

Coloca estos archivos en el mismo directorio que el script del servidor.

---

## **Instalación**

1. Clona o descarga el código fuente del servidor SSH.
2. Coloca el archivo `server_key` en el mismo directorio que el script del servidor.
3. Instala las dependencias necesarias:

   ```bash
   pip install paramiko tqdm
   ```

---

## **Configuración**

### **1. Parámetros del Servidor**
El servidor escucha en la dirección `0.0.0.0` y el puerto `2222` por defecto. Puedes modificar estos valores en el archivo `ssh_server.py`:

```python
HOST = "0.0.0.0"  # Dirección IP para escuchar
PORT = 2222       # Puerto para escuchar
```

### **2. Autenticación**
El servidor está configurado para usar autenticación por contraseña. Las credenciales predeterminadas son:

- **Usuario**: `admin`
- **Contraseña**: `password`

Puedes modificar estas credenciales en el método `check_auth_password` del servidor:

```python
def check_auth_password(self, username, password):
    if username == "admin" and password == "password":
        return paramiko.AUTH_SUCCESSFUL
    return paramiko.AUTH_FAILED
```

---

## **Uso**

### **1. Ejecutar el Servidor**
Ejecuta el servidor con el siguiente comando:

```bash
python ssh_server.py
```

Deberías ver un mensaje como este:

```
Servidor SSH iniciado en 0.0.0.0:2222
```

### **2. Enviar un Archivo desde el Cliente**
Usa el script del cliente (`ssh_client.py`) para enviar un archivo al servidor. Asegúrate de configurar los siguientes parámetros en el cliente:

```python
HOST = "127.0.0.1"  # Dirección del servidor
PORT = 2222         # Puerto del servidor
USERNAME = "admin"  # Nombre de usuario
PASSWORD = "password"  # Contraseña
FILE_PATH = "archivo.xml"  # Ruta del archivo a enviar
```

Ejecuta el cliente con el siguiente comando:

```bash
python ssh_client.py
```

---

## **Salida Esperada**

### **En el Servidor**
```
Servidor SSH iniciado en 0.0.0.0:2222
Nueva conexión desde ('127.0.0.1', 57604)
Intento de inicio de sesión - Usuario: admin, Contraseña: password
Autenticación exitosa.
Cliente conectado.
Recibiendo archivo...
Progreso: 1024 bytes recibidos
Progreso: 2048 bytes recibidos
...
Archivo recibido completamente.
Archivo XML guardado como ./uploads/received_file.xml
```

### **En el Cliente**
```
Enviando archivo...
Progreso: 100%|████████████████████████████████████████| 1.23M/1.23M [00:05<00:00, 246kB/s]
Archivo enviado completamente.
Respuesta del servidor: Archivo recibido correctamente.
```

---

## **Características**

### **1. Progreso del Envío**
- **Cliente**: Muestra una barra de progreso usando la biblioteca `tqdm`.
- **Servidor**: Imprime el progreso en tiempo real mostrando cuántos bytes se han recibido.

### **2. Manejo de Errores**
- El servidor y el cliente están diseñados para manejar errores relacionados con la conexión y el envío de archivos.
- Si ocurre un error, se imprime un mensaje descriptivo.

---

## **Solución de Problemas**

### **1. Error: "Socket exception: Se ha forzado la interrupción de una conexión existente por el host remoto"**
- **Causa**: El cliente cerró la conexión antes de que el servidor pudiera completar la comunicación.
- **Solución**:
  - Asegúrate de que el cliente use `channel.shutdown_write()` después de enviar todos los datos.
  - Verifica que el servidor detecte el final del archivo correctamente.

### **2. Error: "private key file is encrypted"**
- **Causa**: La clave privada (`server_key`) está cifrada con una frase de paso.
- **Solución**:
  - Genera una nueva clave sin frase de paso:

    ```bash
    ssh-keygen -t rsa -b 4096 -f server_key -N ""
    ```

### **3. Error: "FileNotFoundError: No such file or directory: 'server_key'"**
- **Causa**: El archivo `server_key` no está en el directorio correcto.
- **Solución**:
  - Asegúrate de que el archivo `server_key` esté en el mismo directorio que el script del servidor.
  - Usa la ruta absoluta si es necesario.

---

## **Contribuciones**

Si encuentras algún problema o tienes sugerencias para mejorar este proyecto, ¡abre un issue o envía un pull request!

---

## **Licencia**

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

Espero que esta documentación sea útil para ti. 😊