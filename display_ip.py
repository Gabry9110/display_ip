from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from subprocess import check_output
from flask import Flask, jsonify
from datetime import datetime
import requests
import time
import threading

porta = 8081  # Porta server HTTP
refresh = 120  # Ogni quanto aggiornarsi, intervallo in secondi
percorso = "/"  # Dove trovare il server, ("http://ip:porta/percorso", specificando "/" sara' necessario solo "http://ip:porta")
app = Flask(__name__)


def get_local_ip():
    try:
        ip_address = check_output(['hostname', '-I'], encoding='utf-8').split()[0]
        return ip_address
    except:
        return "Non disponibile"


def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        public_ip = response.json()['origin']
        return public_ip
    except:
        return "Non disponibile"


@app.route(percorso, methods=['GET'])
def get_ips():
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"local_ip": local_ip, "public_ip": public_ip, "ip_server_port": porta, "last_updated": last_updated})


def display_thread():
    while True:
        local_ip = get_local_ip()
        public_ip = get_public_ip()
        print(f"IP Locale: {local_ip}")
        print(f"IP Pubblico: {public_ip}")

        with canvas(device) as draw:
            draw.text((0, 0), "IP locale:", fill="white")
            draw.text((0, 16), local_ip, fill="white")
            draw.text((0, 32), "IP pubblico:", fill="white")
            draw.text((0, 48), public_ip, fill="white")

        time.sleep(refresh)


if __name__ == "__main__":
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)

    oled = threading.Thread(target=display_thread)
    oled.daemon = True
    oled.start()
    app.run(host="0.0.0.0", port=porta, debug=True, threaded=True)

