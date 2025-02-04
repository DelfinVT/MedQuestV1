# MedQuestV1
# 📡 Transmisión de Cámara de PC a Oculus Quest 2  

Este proyecto permite transmitir la cámara de una PC a las **Oculus Quest 2** utilizando **Python**, **Flask** y **OpenCV**. Se ejecuta un servidor local que envía el video en vivo y puede verse desde el navegador de las Quest.  

## 🚀 **Características**
✅ **Autenticación segura con usuario y contraseña**  
✅ **Protección contra ataques DDoS**  
✅ **Detección automática de conexión por cable (Ethernet o USB)**  
✅ **Compresión de video para optimizar el rendimiento**  
✅ **Soporte para Windows y Linux**  
✅ **Interfaz mejorada con configuraciones de resolución y calidad**  
✅ **Ruta `/status` para ver conexiones activas y bloqueadas**  

## 📌 **Requisitos**  
Asegúrate de tener **Python 3.x** instalado y luego instala las dependencias con:  
```bash
pip install flask opencv-python flask-httpauth netifaces

▶️ Uso
Clona este repositorio

git clone https://github.com/DelfinVT/nombre-del-repo.git
cd nombre-del-repo

Ejecuta el servidor

python server.py

Encuentra la IP de tu PC

    En Windows:

ipconfig

En Linux/macOS:

    ifconfig

    Busca algo como 192.168.X.X.

Accede desde las Oculus Quest 2

    Abre el navegador en las Quest y ve a:

        http://192.168.X.X:5000

        Inicia sesión (admin / 1234).

🛠 Configuraciones Opcionales

Puedes ajustar la resolución y calidad en la URL:

http://192.168.X.X:5000/video?width=1280&height=720&quality=50

    width: Ancho de la imagen (p. ej., 1280)
    height: Alto de la imagen (p. ej., 720)
    quality: Calidad de compresión de la imagen (p. ej., 50 para baja calidad o 100 para máxima calidad)

    Creado por DelfinVT 🚀