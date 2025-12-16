import threading
import time
import sys
import serial
import serial.tools.list_ports
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import keyboard

# ================= CONFIGURAÇÕES =================
BAUDRATE = 115200
SERIAL_KEYWORD = "DECIMAL:"
AUTO_ENTER = True

running = True
ser = None

# ================= FUNÇÕES =================

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    print("[INFO] Portas seriais encontradas:")
    for p in ports:
        print(f"  - {p.device} | {p.description}")
        if 'Arduino' in p.description or 'CH340' in p.description or 'USB' in p.description:
            print(f"[INFO] Usando porta: {p.device}")
            return p.device
    print("[ERRO] Nenhuma porta Arduino encontrada automaticamente")
    return None


def serial_thread():
    global ser, running
    while running:
        try:
            if ser is None or not ser.is_open:
                port = find_arduino_port()
                if port:
                    print(f"[INFO] Abrindo porta {port} @ {BAUDRATE}")
                    ser = serial.Serial(port, BAUDRATE, timeout=1)
                    time.sleep(2)
                else:
                    time.sleep(2)
                    continue

            line = ser.readline().decode(errors='ignore').strip()
            if line:
                print(f"[SERIAL] {line}")

            if SERIAL_KEYWORD in line:
                value = line.split(SERIAL_KEYWORD)[-1].strip()
                value = ''.join(ch for ch in value if ch.isdigit())
                if value:
                    keyboard.write(value)
                    if AUTO_ENTER:
                        keyboard.press_and_release('enter')

        except Exception as e:
            print("[ERRO]", e)
            time.sleep(1)


def create_image():
    img = Image.new('RGB', (64, 64), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    d.rectangle((8, 8, 56, 56), outline=(200, 0, 0), width=4)
    d.text((18, 22), "RF", fill=(255, 255, 255))
    return img


def on_exit(icon, item):
    global running
    running = False
    try:
        if ser and ser.is_open:
            ser.close()
    except:
        pass
    icon.stop()
    sys.exit()

# ================= MAIN =================
if __name__ == '__main__':
    t = threading.Thread(target=serial_thread, daemon=True)
    t.start()

    icon = pystray.Icon(
        'ArduinoKeyboard',
        create_image(),
        'Arduino → Teclado',
        menu=(item('Sair', on_exit),)
    )
    icon.run()
