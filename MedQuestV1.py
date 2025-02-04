import cv2
import os
import netifaces
import time
import threading
from flask import Flask, Response, request, abort, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.middleware.proxy_fix import ProxyFix
from collections import defaultdict

# Configuración del autor
AUTOR = "DelfinVT"

# Configuración de autenticación
USERNAME = "admin"
PASSWORD = "1234"

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)  # Protección extra para IPs detrás de proxies
auth = HTTPBasicAuth()

# Credenciales de usuario
@auth.verify_password
def verify_password(username, password):
    return username == USERNAME and password == PASSWORD

# Protección contra DDoS
request_counts = defaultdict(int)
BLOCKED_IPS = set()
REQUEST_LIMIT = 10  # Máximo de solicitudes por IP en 10 segundos
BLOCK_TIME = 60  # Tiempo de bloqueo en segundos

def reset_request_counts():
    while True:
        time.sleep(10)
        request_counts.clear()

# Iniciar el hilo de reinicio de contadores
threading.Thread(target=reset_request_counts, daemon=True).start()

@app.before_request
def limit_requests():
    ip = request.remote_addr
    if ip in BLOCKED_IPS:
        abort(403, "Acceso bloqueado por actividad sospechosa.")
    
    request_counts[ip] += 1
    if request_counts[ip] > REQUEST_LIMIT:
        BLOCKED_IPS.add(ip)
        print(f"[ALERTA] Bloqueando IP sospechosa: {ip}")
        time.sleep(BLOCK_TIME)
        BLOCKED_IPS.remove(ip)

# Obtener la mejor IP para conexiones cableadas
def get_local_ip():
    interfaces = netifaces.interfaces()
    preferidas = ["eth0", "en0", "wlan0", "wlp2s0"]  # Ethernet y WiFi común
    for iface in preferidas:
        if iface in interfaces:
            addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET, [])
            if addrs:
                return addrs[0]['addr']
    return "127.0.0.1"

# Generador de frames con compresión
def generate_frames(resolution=(640, 480), quality=80):
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, buffer = cv2.imencode('.jpg', frame, encode_param)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Ruta para ver el video con autenticación
@app.route('/video')
@auth.login_required
def video_feed():
    width = int(request.args.get("width", 640))
    height = int(request.args.get("height", 480))
    quality = int(request.args.get("quality", 80))
    return Response(generate_frames((width, height), quality), mimetype='multipart/x-mixed-replace; boundary=frame')

# Página principal con mensaje de seguridad y autor
@app.route('/')
@auth.login_required
def index():
    return f'''
    <html>
        <head>
            <title>Streaming de Cámara</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: #222;
                    color: #fff;
                }}
                h1 {{ color: #00bfff; }}
                img {{ border: 4px solid #00bfff; border-radius: 10px; }}
                input, button {{
                    padding: 10px;
                    margin: 5px;
                    border: none;
                    border-radius: 5px;
                }}
                button {{ background-color: #00bfff; color: #fff; cursor: pointer; }}
            </style>
        </head>
        <body>
            <h1>Transmisión en Vivo</h1>
            <p>Desarrollado por <b>DelfinVT</b></p>
            <p>Protección activa contra ataques DDoS ✅</p>
            <form action="/video" method="get">
                <label for="width">Ancho:</label>
                <input type="number" name="width" value="640">
                <label for="height">Alto:</label>
                <input type="number" name="height" value="480">
                <label for="quality">Calidad (1-100):</label>
                <input type="number" name="quality" value="80">
                <button type="submit">Ver Stream</button>
            </form>
            <br>
            <img src="/video" width="640" height="480">
        </body>
    </html>
    '''

# Ruta para verificar estado del servidor
@app.route('/status')
def status():
    return jsonify({
        "status": "online",
        "author": "DelfinVT",
        "active_connections": len(request_counts),
        "blocked_ips": list(BLOCKED_IPS)
    })

if __name__ == '__main__':
    ip = get_local_ip()
    print(f"""
    ┌──────────────────────────────────────────────┐
    │        🚀 Streaming de Cámara Activo        │
    │        Desarrollado por DelfinVT           │
    │  Accede en: http://{ip}:5000               │
    └──────────────────────────────────────────────┘
    """)
    app.run(host='0.0.0.0', port=5000, debug=False)
