import threading
import time
from sensors_list import *

# SW-Req: [SW-ID-21]
class Modo1Monitor:
    def __init__(self, root, alert_callback):
        self.root = root
        self.alert_callback = alert_callback
        self.running = False
        self.thread = None
        self.check_interval = 0.5  # Medio segundo
        self.s1_delay = 5  # Segundos de retardo para S1
        self.s1_timer = None
        self.current_state = "monitoring"  # monitoring/delayed/alerting
        self.special_sensors = ["S1"]  # Sensores que se monitorean sin importar su zona

    # SW-Req: [SW-ID-73]
    # SW-Req: [SW-ID-44]
    def start_monitoring(self):
        """Inicia el hilo de monitoreo"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            print("[MODO 1] Monitoreo iniciado")

    def stop_monitoring(self):
        """Detiene el monitoreo de manera segura"""
        if self.running:
            self.running = False
            self._cancel_s1_delay()
            if self.thread:
                self.thread.join()
            print("[MODO 1] Monitoreo detenido")

    def _monitor_loop(self):
        """Bucle principal de monitoreo"""
        while self.running:
            if self.current_state == "monitoring":
                triggered_sensors = self._check_activated_sensors()
                
                if triggered_sensors:
                    if "S1" in triggered_sensors:
                        self._handle_s1_delay()
                    else:
                        self._trigger_immediate_alert(triggered_sensors)
            
            time.sleep(self.check_interval)

    def _handle_s1_delay(self):
        """Maneja el retardo especial para S1 aunque esté en Zona 0"""
        self.current_state = "delayed"
        print(f"[MODO 1] Sensor S1 activado (Zona {Sensors_list['S1']['Zone']}). Esperando {self.s1_delay}s...")
        self.s1_timer = threading.Timer(
            self.s1_delay, 
            lambda: self._trigger_delayed_alert("S1")
        )
        self.s1_timer.start()

    def _trigger_immediate_alert(self, sensors):
        """Activa alerta inmediata para sensores que no son S1"""
        self.current_state = "alerting"
        self.root.after(0, lambda: self.alert_callback(sensors))
        print(f"[MODO 1] Alerta inmediata activada para sensores: {', '.join(sensors)}")

    def _trigger_delayed_alert(self, sensor):
        """Activa alerta después del retardo para S1"""
        if self.running and self.current_state == "delayed":
            self.current_state = "alerting"
            self.root.after(0, lambda: self.alert_callback([sensor]))
            print(f"[MODO 1] Alerta retardada activada para sensor: {sensor}")

    def _cancel_s1_delay(self):
        """Cancela el retardo si se desarma el sistema"""
        if self.s1_timer and self.s1_timer.is_alive():
            self.s1_timer.cancel()
            print("[MODO 1] Retardo S1 cancelado (sistema desarmado)")
        self.current_state = "monitoring"

    def _check_activated_sensors(self):
        """
        Retorna lista de sensores activados que cumplen:
        - Install = INSTALL
        - Status = ACTIVE
        - Zone = ZONE_1 o es un sensor especial (como S1)
        """
        triggered = []
        
        # SW-Req: [SW-ID-5]
        for sensor_name, sensor_data in Sensors_list.items():
            if (sensor_data["Install"] == INSTALL and
                sensor_data["Status"] == ACTIVE):
                
                # SW-Req: [SW-ID-35]
                # SW-Req: [SW-ID-36]
                if (sensor_data["Zone"] == ZONE_1 or 
                    sensor_name in self.special_sensors):
                    triggered.append(sensor_name)
        
        return triggered

    def check_desarmado_during_delay(self):
        """Para ser llamado cuando se ingresa código de desarmado"""
        if self.current_state == "delayed":
            self._cancel_s1_delay()
            print("[MODO 1] Alerta cancelada durante retardo S1")

    def add_special_sensor(self, sensor_name):
        """Añade un sensor a la lista de especiales"""
        if sensor_name not in self.special_sensors:
            self.special_sensors.append(sensor_name)
            print(f"[MODO 1] Sensor {sensor_name} añadido a monitoreo especial")

    def remove_special_sensor(self, sensor_name):
        """Remueve un sensor de la lista de especiales"""
        if sensor_name in self.special_sensors:
            self.special_sensors.remove(sensor_name)
            print(f"[MODO 1] Sensor {sensor_name} removido de monitoreo especial")